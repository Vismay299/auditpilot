"""
Finalize an inspection after all files have been processed.
Calculates risk level, generates narrative, and updates the inspection record.
"""
import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.finding_repository import FindingRepository
from app.repositories.inspection_repository import InspectionRepository
from app.services.hf_client import HFInferenceClient

logger = logging.getLogger(__name__)

SEVERITY_WEIGHTS = {
    "critical": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "clear": 0,
}


class InspectionCompletionService:
    def __init__(self, db: Session, hf: HFInferenceClient):
        self.db = db
        self.finding_repo = FindingRepository(db)
        self.inspection_repo = InspectionRepository(db)
        self.hf = hf

    async def finalize(self, inspection_id: UUID) -> None:
        """Run after all files are processed: compute risk, narrative, mark complete."""
        findings = self.finding_repo.list_by_inspection(inspection_id)
        total_findings = len(findings)
        inspection = self.inspection_repo.get_by_id(inspection_id)

        if not inspection:
            logger.error("Inspection %s not found", inspection_id)
            return

        # 1. Risk level from severity distribution
        risk_level = self._calculate_risk(findings)

        # 2. Generate narrative
        narrative = await self._generate_narrative(findings, inspection)

        # 3. Check if any need human review
        needs_review = any(getattr(f, "needs_review", False) for f in findings)
        status = "review" if needs_review else "completed"

        # 4. Update inspection record
        self.inspection_repo.update_status(
            inspection_id,
            status=status,
            risk_level=risk_level,
            report_narrative=narrative,
            total_findings=total_findings,
            processing_completed_at=datetime.now(timezone.utc),
        )
        logger.info(
            "Inspection %s finalized: risk=%s findings=%d status=%s",
            inspection_id, risk_level, total_findings, status,
        )

    def _calculate_risk(self, findings: list) -> str:
        """Highest severity among findings wins."""
        if not findings:
            return "clear"

        max_weight = 0
        for f in findings:
            sev = getattr(f, "severity", None) or "clear"
            max_weight = max(max_weight, SEVERITY_WEIGHTS.get(sev, 0))

        # Map weight back to label
        for label, weight in SEVERITY_WEIGHTS.items():
            if weight == max_weight:
                return label
        return "clear"

    async def _generate_narrative(self, findings: list, inspection) -> str:
        """Generate report narrative using BART-CNN summarization."""
        if not findings:
            return "No findings were detected during this inspection. All uploaded files were analyzed and no defects or hazards were identified."

        # Build context from findings
        lines: list[str] = []
        name = getattr(inspection, "name", "Inspection")
        location = getattr(inspection, "site_location", "")
        lines.append(f"Inspection: {name}. Location: {location}.")

        for i, f in enumerate(findings, 1):
            category = getattr(f, "category", "unknown")
            severity = getattr(f, "severity", "unknown")
            caption = getattr(f, "ai_caption", "") or ""
            transcription = getattr(f, "transcription", "") or ""
            desc = caption or transcription
            lines.append(f"Finding {i}: {category} ({severity}). {desc}")

        context = " ".join(lines)

        # BART-CNN can handle ~1024 tokens, truncate if needed
        if len(context) > 3000:
            context = context[:3000]

        try:
            result = await self.hf.inference_json(
                "facebook/bart-large-cnn",
                {
                    "inputs": context,
                    "parameters": {
                        "max_length": 400,
                        "min_length": 80,
                        "do_sample": False,
                    },
                },
            )
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("summary_text", context)
            return context
        except Exception as exc:
            logger.warning("Narrative generation failed, using raw context: %s", exc)
            return context
