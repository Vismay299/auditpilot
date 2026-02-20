"use client";

import { useCallback, useEffect, useState } from "react";
import { api, type FileRecord } from "@/lib/api/client";
import { Badge } from "@/components/ui/badge";
import { Loader2, FileImage, FileAudio, FileText } from "lucide-react";

type Props = {
  inspectionId: string;
  refreshInterval?: number;
};

function statusVariant(status: string): "default" | "secondary" | "destructive" | "outline" {
  switch (status) {
    case "completed":
      return "default";
    case "failed":
      return "destructive";
    case "processing":
      return "secondary";
    default:
      return "outline";
  }
}

function FileIcon({ type }: { type: string }) {
  if (type === "image") return <FileImage className="h-4 w-4" />;
  if (type === "audio") return <FileAudio className="h-4 w-4" />;
  return <FileText className="h-4 w-4" />;
}

export function FileStatusList({ inspectionId, refreshInterval = 3000 }: Props) {
  const [files, setFiles] = useState<FileRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFiles = useCallback(() => {
    api
      .listFiles(inspectionId)
      .then((r) => setFiles(r.files))
      .catch(() => setFiles([]))
      .finally(() => setLoading(false));
  }, [inspectionId]);

  useEffect(() => {
    fetchFiles();
    if (refreshInterval > 0) {
      const id = setInterval(fetchFiles, refreshInterval);
      return () => clearInterval(id);
    }
  }, [fetchFiles, refreshInterval]);

  if (loading && files.length === 0) {
    return (
      <div className="flex items-center gap-2 text-muted-foreground">
        <Loader2 className="h-4 w-4 animate-spin" />
        Loading files…
      </div>
    );
  }

  if (files.length === 0) {
    return <p className="text-sm text-muted-foreground">No files uploaded yet.</p>;
  }

  return (
    <ul className="space-y-2 max-h-60 overflow-auto">
      {files.map((f) => (
        <li
          key={f.id}
          className="flex items-center justify-between gap-2 rounded border px-3 py-2 text-sm"
        >
          <div className="flex items-center gap-2 min-w-0">
            <FileIcon type={f.file_type} />
            <span className="truncate">{f.file_name}</span>
          </div>
          <Badge variant={statusVariant(f.status)}>{f.status}</Badge>
        </li>
      ))}
    </ul>
  );
}
