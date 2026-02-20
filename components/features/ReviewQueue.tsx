"use client";

import { useEffect, useState } from "react";
import { api, type Finding } from "@/lib/api/client";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

type QueueItem = Finding & { inspection: { id: string; name: string } };

export function ReviewQueue() {
    const [findings, setFindings] = useState<QueueItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getReviewQueue()
            .then(setFindings)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="border-b border-border/50 bg-muted/20">
                <CardTitle>Pending Reviews</CardTitle>
                <CardDescription>AI findings flagged with low confidence ({findings.length})</CardDescription>
            </CardHeader>
            <CardContent className="flex-1 p-0 overflow-auto">
                {loading ? (
                    <div className="p-6 text-sm text-muted-foreground flex justify-center">Loading queue...</div>
                ) : findings.length === 0 ? (
                    <div className="p-6 text-sm text-muted-foreground flex justify-center items-center h-full">All caught up! No findings require manual review.</div>
                ) : (
                    <div className="w-full">
                        <table className="w-full text-sm text-left">
                            <thead className="text-xs text-muted-foreground uppercase bg-muted/20 sticky top-0">
                                <tr>
                                    <th className="px-6 py-3 font-medium">Inspection</th>
                                    <th className="px-6 py-3 font-medium">Finding Detail</th>
                                    <th className="px-6 py-3 font-medium">AI Confidence</th>
                                    <th className="px-6 py-3 font-medium text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border">
                                {findings.map((f) => (
                                    <tr key={f.id} className="hover:bg-muted/10 transition-colors">
                                        <td className="px-6 py-4 font-medium whitespace-nowrap">
                                            <Link href={`/inspection/${f.inspection.id}`} className="hover:underline text-blue-600 font-semibold">
                                                {f.inspection.name}
                                            </Link>
                                            <div className="text-xs text-muted-foreground mt-1 lowercase">
                                                <Badge variant="outline" className="text-[10px] px-1.5 py-0 uppercase">{f.category}</Badge>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 max-w-[200px]">
                                            <p className="truncate" title={f.ai_caption || f.description || ""}>
                                                {f.ai_caption || f.description || "N/A"}
                                            </p>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {f.confidence_score !== null ? (
                                                <span className={f.confidence_score < 0.6 ? "text-red-500 font-semibold bg-red-50 px-2 py-1 rounded" : ""}>
                                                    {(f.confidence_score * 100).toFixed(1)}%
                                                </span>
                                            ) : "N/A"}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right">
                                            <Button size="sm" variant="secondary" className="shadow-sm" asChild>
                                                <Link href={`/inspection/${f.inspection.id}`}>Review</Link>
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
