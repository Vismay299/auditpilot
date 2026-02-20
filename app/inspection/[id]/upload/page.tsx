"use client";

import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileUpload } from "@/components/features/FileUpload";
import { FileStatusList } from "@/components/features/FileStatusList";
import { ArrowLeft, FileUp } from "lucide-react";

export default function UploadPage() {
  const params = useParams();
  const router = useRouter();
  const inspectionId = params.id as string;

  if (!inspectionId) {
    return (
      <div className="container mx-auto py-8 px-4">
        <p className="text-muted-foreground">Missing inspection ID.</p>
        <Button variant="link" asChild>
          <Link href="/dashboard">Back to dashboard</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-6 flex items-center gap-4">
        <Button variant="ghost" size="icon" asChild>
          <Link href="/dashboard">
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Upload files</h1>
          <p className="text-muted-foreground">
            Add photos, audio recordings, and documents for this inspection.
          </p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileUp className="h-5 w-5" />
              Upload files
            </CardTitle>
          </CardHeader>
          <CardContent>
            <FileUpload inspectionId={inspectionId} onUploadComplete={() => {}} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Processing status</CardTitle>
          </CardHeader>
          <CardContent>
            <FileStatusList inspectionId={inspectionId} refreshInterval={3000} />
          </CardContent>
        </Card>
      </div>

      <div className="mt-6 flex justify-end">
        <Button asChild>
          <Link href={`/inspection/${inspectionId}`}>View report</Link>
        </Button>
      </div>
    </div>
  );
}
