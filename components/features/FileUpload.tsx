"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { api } from "@/lib/api/client";
import { Upload, X } from "lucide-react";

const MAX_SIZE = 50 * 1024 * 1024; // 50MB
const ACCEPT = {
  "image/*": [".jpg", ".jpeg", ".png"],
  "audio/*": [".mp3", ".m4a", ".wav"],
  "application/pdf": [".pdf"],
};

type Props = {
  inspectionId: string;
  onUploadComplete?: () => void;
};

export function FileUpload({ inspectionId, onUploadComplete }: Props) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [queued, setQueued] = useState<File[]>([]);

  const onDrop = useCallback((accepted: File[]) => {
    setQueued((prev) => [...prev, ...accepted]);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPT,
    maxSize: MAX_SIZE,
    multiple: true,
    disabled: uploading,
  });

  const removeQueued = (index: number) => {
    setQueued((prev) => prev.filter((_, i) => i !== index));
  };

  const startUpload = async () => {
    if (queued.length === 0) return;
    setUploading(true);
    setError(null);
    setProgress(0);
    try {
      await api.uploadFiles(inspectionId, queued, (loaded: number, total: number) => {
        setProgress(total ? Math.round((loaded / total) * 100) : 0);
      });
      setQueued([]);
      onUploadComplete?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25 hover:border-primary/50"
          }`}
      >
        <input {...getInputProps()} />
        <Upload className="h-10 w-10 mx-auto text-muted-foreground mb-2" />
        <p className="text-sm text-muted-foreground">
          {isDragActive ? "Drop files here" : "Drag & drop images, audio, or PDFs here, or click to select"}
        </p>
        <p className="text-xs text-muted-foreground mt-1">Max 50MB per file</p>
      </div>

      {queued.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium">{queued.length} file(s) ready</p>
          <ul className="space-y-1 max-h-40 overflow-auto">
            {queued.map((f, i) => (
              <li key={i} className="flex items-center justify-between text-sm">
                <span className="truncate">{f.name}</span>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7"
                  onClick={() => removeQueued(i)}
                  disabled={uploading}
                >
                  <X className="h-4 w-4" />
                </Button>
              </li>
            ))}
          </ul>
          {uploading && <Progress value={progress} className="h-2" />}
          <Button onClick={startUpload} disabled={uploading} className="w-full">
            {uploading ? `Uploading… ${progress}%` : "Upload all"}
          </Button>
        </div>
      )}

      {error && <p className="text-sm text-destructive">{error}</p>}
    </div>
  );
}
