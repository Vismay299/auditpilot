"""
Background file processing: called by FastAPI BackgroundTasks after upload.
Runs ML pipelines to generate findings from uploaded files.
"""
import asyncio
import logging
import time
from uuid import UUID

from app.core.database import SessionLocal
from app.repositories.file_repository import FileRepository
from app.repositories.finding_repository import FindingRepository
from app.services.hf_client import HFInferenceClient
from app.services.image_processor import ImageProcessor
from app.services.audio_processor import AudioProcessor
from app.services.pdf_processor import PdfProcessor
from app.services.embedding_service import EmbeddingService
from app.services.inspection_completion_service import InspectionCompletionService
from app.services.storage_service import download_file
from app.services.job_tracker import JobTracker

logger = logging.getLogger(__name__)


def process_file_background(file_id: str, file_type: str, inspection_id: str) -> None:
    """
    Synchronous entry point for FastAPI BackgroundTasks.
    Creates its own DB session and processes one file.
    """
    asyncio.run(_process_file(file_id, file_type, inspection_id))


async def _process_file(file_id: str, file_type: str, inspection_id: str) -> None:
    db = SessionLocal()
    hf = HFInferenceClient()
    try:
        tracker = JobTracker(db)
        file_repo = FileRepository(db)
        finding_repo = FindingRepository(db)
        file_uuid = UUID(file_id)
        inspection_uuid = UUID(inspection_id)

        tracker.update_file_status(file_uuid, "processing")
        start = time.monotonic()

        try:
            # Get file record for storage key
            file_record = file_repo.get_by_id(file_uuid)
            if not file_record:
                raise ValueError(f"File record not found: {file_id}")

            # Download file bytes from local storage
            file_bytes = await download_file(file_record.storage_key)

            # Route to appropriate pipeline
            if file_type == "image":
                await _process_image(hf, finding_repo, file_uuid, inspection_uuid, file_bytes)
            elif file_type == "audio":
                await _process_audio(hf, finding_repo, file_uuid, inspection_uuid, file_bytes)
            elif file_type == "pdf":
                await _process_pdf(hf, finding_repo, file_uuid, inspection_uuid, file_bytes)
            else:
                logger.info("No ML pipeline for file_type=%s, marking complete", file_type)

        except Exception as e:
            logger.exception("Processing failed for file_id=%s", file_id)
            tracker.update_file_status(file_uuid, "failed", error_message=str(e))
            return

        tracker.update_file_status(file_uuid, "completed")
        tracker.update_inspection_progress(inspection_uuid)

        duration = time.monotonic() - start
        logger.info("file_id=%s pipeline completed in %.2fs", file_id, duration)

        # Check if all files are done → finalize inspection
        total = file_repo.total_count_by_inspection(inspection_uuid)
        completed = file_repo.count_by_inspection_and_status(inspection_uuid, "completed")
        failed = file_repo.count_by_inspection_and_status(inspection_uuid, "failed")

        if completed + failed >= total:
            completion = InspectionCompletionService(db, hf)
            await completion.finalize(inspection_uuid)
    finally:
        await hf.close()
        db.close()


async def _process_image(
    hf: HFInferenceClient,
    finding_repo: FindingRepository,
    file_id: UUID,
    inspection_id: UUID,
    image_bytes: bytes,
) -> None:
    """Image pipeline: BLIP caption → BART classify → embed → create Finding."""
    img_proc = ImageProcessor(hf)
    embed_svc = EmbeddingService(hf)

    try:
        # 1. Caption
        caption = await img_proc.generate_caption(image_bytes)
        logger.info("file_id=%s caption: %s", file_id, caption[:100])

        # 2. Classify
        classification = await img_proc.classify_text(caption)

        # 3. Embed
        embedding = await embed_svc.generate_embedding(caption)

        # 4. Create Finding
        finding_repo.create(
            inspection_id=inspection_id,
            file_id=file_id,
            category=classification["category"],
            severity=classification["severity"],
            confidence_score=classification["confidence"],
            needs_review=classification["needs_review"],
            ai_caption=caption,
            description=f"Image classified as {classification['category']} with {classification['confidence']:.0%} confidence.",
            extra_metadata=classification.get("all_scores", {}),
            embedding=embedding,
        )
        logger.info("file_id=%s finding created: %s (%s)", file_id, classification["category"], classification["severity"])
    except Exception as exc:
        # Keep the pipeline resilient when upstream caption models are unavailable.
        logger.warning("file_id=%s image pipeline fallback due to error: %s", file_id, exc)
        finding_repo.create(
            inspection_id=inspection_id,
            file_id=file_id,
            category="clear/no defect",
            severity="clear",
            confidence_score=0.0,
            needs_review=True,
            ai_caption=None,
            description="Automatic image captioning was unavailable for this file. Manual review required.",
            extra_metadata={"pipeline_error": str(exc)},
            embedding=[0.0] * 384,
        )
        logger.info("file_id=%s fallback finding created (needs_review=true)", file_id)


async def _process_audio(
    hf: HFInferenceClient,
    finding_repo: FindingRepository,
    file_id: UUID,
    inspection_id: UUID,
    audio_bytes: bytes,
) -> None:
    """Audio pipeline: Whisper transcribe → BART classify → embed → create Finding."""
    audio_proc = AudioProcessor(hf)
    embed_svc = EmbeddingService(hf)

    # 1. Transcribe
    transcription = await audio_proc.transcribe(audio_bytes)
    logger.info("file_id=%s transcription: %s", file_id, transcription[:100] if transcription else "(empty)")

    # 2. Classify
    classification = await audio_proc.classify_transcription(transcription)

    # 3. Embed
    embedding = await embed_svc.generate_embedding(transcription)

    # 4. Create Finding
    finding_repo.create(
        inspection_id=inspection_id,
        file_id=file_id,
        category=classification["category"],
        severity=classification["severity"],
        confidence_score=classification["confidence"],
        needs_review=classification["needs_review"],
        transcription=transcription,
        description=f"Audio transcribed and classified as {classification['category']}.",
        extra_metadata=classification.get("all_scores", {}),
        embedding=embedding,
    )
    logger.info("file_id=%s audio finding created: %s", file_id, classification["category"])


async def _process_pdf(
    hf: HFInferenceClient,
    finding_repo: FindingRepository,
    file_id: UUID,
    inspection_id: UUID,
    pdf_bytes: bytes,
) -> None:
    """PDF pipeline: pypdf extract → BART classify → embed → create Finding."""
    pdf_proc = PdfProcessor(hf)
    embed_svc = EmbeddingService(hf)

    # 1. Extract text
    text = await pdf_proc.extract_text(pdf_bytes)
    logger.info("file_id=%s extracted %d chars from PDF", file_id, len(text))

    # 2. Classify
    classification = await pdf_proc.classify_text(text)

    # 3. Embed (use first 2000 chars for embedding)
    embedding = await embed_svc.generate_embedding(text[:2000])

    # 4. Create Finding
    finding_repo.create(
        inspection_id=inspection_id,
        file_id=file_id,
        category=classification["category"],
        severity=classification["severity"],
        confidence_score=classification["confidence"],
        needs_review=classification["needs_review"],
        description=f"PDF analyzed and classified as {classification['category']}.",
        extra_metadata={
            "text_length": len(text),
            "preview": text[:500],
            **classification.get("all_scores", {}),
        },
        embedding=embedding,
    )
    logger.info("file_id=%s PDF finding created: %s", file_id, classification["category"])
