"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Inspection } from "@/lib/api/client";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { NewInspectionDialog } from "@/components/features/NewInspectionDialog";
import { StatsCard } from "@/components/features/StatsCard";
import { FindingsChart } from "@/components/features/FindingsChart";
import { ReviewQueue } from "@/components/features/ReviewQueue";
import { CostTracker } from "@/components/features/CostTracker";
import { ClipboardList, Plus, FileText, AlertCircle } from "lucide-react";

function statusVariant(status: string): "default" | "secondary" | "destructive" | "outline" {
  switch (status) {
    case "completed":
      return "default";
    case "review":
      return "secondary";
    case "failed":
      return "destructive";
    default:
      return "outline";
  }
}

export default function DashboardPage() {
  const [inspections, setInspections] = useState<Inspection[]>([]);
  const [stats, setStats] = useState<{ totalInspections: number; totalFindings: number; pendingReviews: number } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      api.listInspections(),
      api.getInspectionStats()
    ])
      .then(([insps, st]) => {
        setInspections(insps);
        setStats(st);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const handleNewInspection = (inspectionId: string) => {
    setDialogOpen(false);
    window.location.href = `/inspection/${inspectionId}/upload`;
  };

  const refreshList = () => {
    setLoading(true);
    setError(null);
    Promise.all([
      api.listInspections(),
      api.getInspectionStats()
    ])
      .then(([insps, st]) => {
        setInspections(insps);
        setStats(st);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">Overview of your inspections</p>
        </div>
        <NewInspectionDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          onSuccess={handleNewInspection}
        />
        <Button onClick={() => setDialogOpen(true)} className="gap-2">
          <Plus className="h-4 w-4" />
          New inspection
        </Button>
      </div>

      {/* Stats Row */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-6">
        <StatsCard
          title="Total Inspections"
          value={loading ? "-" : stats?.totalInspections || 0}
          icon={ClipboardList}
        />
        <StatsCard
          title="Total Findings"
          value={loading ? "-" : stats?.totalFindings || 0}
          icon={FileText}
        />
        <StatsCard
          title="Pending Reviews"
          value={loading ? "-" : stats?.pendingReviews || 0}
          icon={AlertCircle}
          trendUp={false}
          trend={stats?.pendingReviews ? "Needs attention" : ""}
        />
        <CostTracker inspectionsCount={stats?.totalInspections || 0} />
      </div>

      {/* Analytics Row */}
      <div className="grid gap-6 md:grid-cols-3 mb-6">
        <div className="md:col-span-2">
          <ReviewQueue />
        </div>
        <div className="md:col-span-1 min-h-[400px]">
          <FindingsChart />
        </div>
      </div>

      <div className="grid gap-6 mt-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between border-b border-border/50 bg-muted/20">
            <CardTitle className="flex items-center gap-2">
              <ClipboardList className="h-5 w-5" />
              Recent inspections
            </CardTitle>
            <Button variant="outline" size="sm" onClick={refreshList} disabled={loading}>
              Refresh
            </Button>
          </CardHeader>
          <CardContent className="pt-6">
            {error && (
              <p className="text-sm text-destructive mb-4">
                {error}. Ensure backend is running and you are logged in.
              </p>
            )}
            {loading ? (
              <p className="text-muted-foreground">Loading...</p>
            ) : inspections.length === 0 ? (
              <p className="text-muted-foreground">
                No inspections yet. Create one to upload files and generate reports.
              </p>
            ) : (
              <ul className="space-y-3">
                {inspections.map((i) => (
                  <li key={i.id}>
                    <Link
                      href={`/inspection/${i.id}/upload`}
                      className="flex items-center justify-between rounded-lg border p-4 transition-colors hover:bg-muted/50"
                    >
                      <div>
                        <p className="font-medium text-blue-600 hover:underline">{i.name}</p>
                        <p className="text-sm text-muted-foreground mt-1">
                          {i.site_location || "No location"} · {i.total_files} files
                          {i.total_findings > 0 && ` · ${i.total_findings} findings`}
                        </p>
                      </div>
                      <Badge variant={statusVariant(i.status)} className="capitalize">{i.status}</Badge>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
