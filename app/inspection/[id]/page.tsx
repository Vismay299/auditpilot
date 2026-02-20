"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api, type Inspection, type Finding } from "@/lib/api/client";
import {
  ArrowLeft,
  FileText,
  AlertTriangle,
  CheckCircle2,
  Eye,
  Image,
  Mic,
  FileIcon,
  Shield,
} from "lucide-react";

function severityColor(severity: string | null) {
  switch (severity) {
    case "critical":
      return "bg-red-600 text-white";
    case "high":
      return "bg-orange-500 text-white";
    case "medium":
      return "bg-yellow-500 text-black";
    case "low":
      return "bg-blue-400 text-white";
    case "clear":
      return "bg-green-500 text-white";
    default:
      return "bg-gray-400 text-white";
  }
}

function riskColor(risk: string | null) {
  switch (risk) {
    case "critical":
      return "destructive";
    case "high":
      return "destructive";
    case "medium":
      return "secondary";
    case "low":
      return "outline";
    case "clear":
      return "outline";
    default:
      return "outline";
  }
}

function FindingIcon({ category }: { category: string }) {
  if (category.includes("electrical") || category.includes("fire"))
    return <AlertTriangle className="h-4 w-4 text-orange-500" />;
  if (category.includes("clear"))
    return <CheckCircle2 className="h-4 w-4 text-green-500" />;
  return <Shield className="h-4 w-4 text-red-500" />;
}

export default function InspectionReportPage() {
  const params = useParams();
  const id = params.id as string;
  const [inspection, setInspection] = useState<Inspection | null>(null);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    const load = async () => {
      try {
        const [insp, findingsRes] = await Promise.all([
          api.getInspection(id),
          api.listFindings(id),
        ]);
        setInspection(insp);
        setFindings(findingsRes.findings);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    };

    load();
    // Poll while processing
    const interval = setInterval(async () => {
      try {
        const [insp, findingsRes] = await Promise.all([
          api.getInspection(id),
          api.listFindings(id),
        ]);
        setInspection(insp);
        setFindings(findingsRes.findings);
        if (insp.status === "completed" || insp.status === "review") {
          clearInterval(interval);
        }
      } catch {
        /* ignore polling errors */
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [id]);

  if (!id) {
    return (
      <div className="container mx-auto py-8 px-4">
        <p className="text-muted-foreground">Missing inspection ID.</p>
        <Button variant="link" asChild>
          <Link href="/dashboard">Back to dashboard</Link>
        </Button>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8 px-4">
        <p className="text-destructive">{error}</p>
        <Button variant="link" asChild>
          <Link href="/dashboard">Back to dashboard</Link>
        </Button>
      </div>
    );
  }

  if (loading || !inspection) {
    return (
      <div className="container mx-auto py-8 px-4">
        <p className="text-muted-foreground">Loading report…</p>
      </div>
    );
  }

  const isProcessing = inspection.status === "processing";

  return (
    <div className="container mx-auto py-8 px-4">
      {/* Header */}
      <div className="mb-6 flex items-center gap-4">
        <Button variant="ghost" size="icon" asChild>
          <Link href={`/inspection/${id}/upload`}>
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold tracking-tight">{inspection.name}</h1>
          <p className="text-muted-foreground">
            {inspection.site_location || "No location"}
            {inspection.site_address && ` · ${inspection.site_address}`}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {inspection.risk_level && (
            <Badge variant={riskColor(inspection.risk_level) as "destructive" | "secondary" | "outline"}>
              Risk: {inspection.risk_level}
            </Badge>
          )}
          <Badge variant="outline">{inspection.status}</Badge>
        </div>
      </div>

      {/* Processing Banner */}
      {isProcessing && (
        <Card className="mb-6 border-blue-200 bg-blue-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="animate-spin h-5 w-5 rounded-full border-2 border-blue-500 border-t-transparent" />
              <p className="text-blue-700">
                Files are being processed by the ML pipeline. This page will update automatically…
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Summary */}
      <div className="grid gap-6 md:grid-cols-3 mb-6">
        <Card>
          <CardContent className="pt-6 text-center">
            <p className="text-3xl font-bold">{inspection.total_files}</p>
            <p className="text-sm text-muted-foreground">Files</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <p className="text-3xl font-bold">{inspection.total_findings}</p>
            <p className="text-sm text-muted-foreground">Findings</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <p className={`text-3xl font-bold capitalize ${inspection.risk_level === "critical" || inspection.risk_level === "high" ? "text-red-600" : inspection.risk_level === "clear" ? "text-green-600" : ""}`}>
              {inspection.risk_level || "–"}
            </p>
            <p className="text-sm text-muted-foreground">Risk Level</p>
          </CardContent>
        </Card>
      </div>

      {/* Narrative */}
      {inspection.report_narrative && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Report Narrative
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed whitespace-pre-line">
              {inspection.report_narrative}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Findings */}
      {findings.length > 0 && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Findings ({findings.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {findings.map((f) => (
                <div
                  key={f.id}
                  className="flex items-start gap-4 p-4 rounded-lg border"
                >
                  <FindingIcon category={f.category} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium capitalize">{f.category}</span>
                      <span
                        className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${severityColor(f.severity)}`}
                      >
                        {f.severity}
                      </span>
                      {f.confidence_score != null && (
                        <span className="text-xs text-muted-foreground">
                          {Math.round(f.confidence_score * 100)}% confidence
                        </span>
                      )}
                      {f.needs_review && (
                        <Badge variant="outline" className="text-xs">
                          <Eye className="h-3 w-3 mr-1" />
                          Needs review
                        </Badge>
                      )}
                    </div>
                    {f.ai_caption && (
                      <p className="text-sm text-muted-foreground flex items-start gap-1">
                        <Image className="h-3 w-3 mt-0.5 shrink-0" /> {f.ai_caption}
                      </p>
                    )}
                    {f.transcription && (
                      <p className="text-sm text-muted-foreground flex items-start gap-1">
                        <Mic className="h-3 w-3 mt-0.5 shrink-0" /> {f.transcription.slice(0, 300)}{f.transcription.length > 300 ? "…" : ""}
                      </p>
                    )}
                    {f.description && !f.ai_caption && !f.transcription && (
                      <p className="text-sm text-muted-foreground flex items-start gap-1">
                        <FileIcon className="h-3 w-3 mt-0.5 shrink-0" /> {f.description}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* No findings yet */}
      {!isProcessing && findings.length === 0 && (
        <Card className="mb-6">
          <CardContent className="pt-6 text-center">
            <CheckCircle2 className="h-8 w-8 mx-auto mb-2 text-green-500" />
            <p className="text-muted-foreground">No findings detected. Upload files to begin analysis.</p>
          </CardContent>
        </Card>
      )}

      {/* Actions */}
      <div className="flex gap-4">
        <Button asChild variant="outline">
          <Link href={`/inspection/${id}/upload`}>Upload more files</Link>
        </Button>
        <Button asChild>
          <Link href="/dashboard">Dashboard</Link>
        </Button>
      </div>
    </div>
  );
}
