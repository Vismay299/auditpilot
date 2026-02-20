"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { api } from "@/lib/api/client";

const COLORS: Record<string, string> = {
    "Structural": "#ef4444",
    "Electrical": "#f59e0b",
    "Water": "#3b82f6",
    "Fire": "#dc2626",
    "Clear": "#10b981",
    "Unknown": "#94a3b8"
};

export function FindingsChart() {
    const [data, setData] = useState<{ name: string, value: number }[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getFindingsStats()
            .then(setData)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return (
        <Card className="flex flex-col h-full">
            <CardHeader className="pb-0 border-b border-border/50 bg-muted/20">
                <CardTitle>Findings Distribution</CardTitle>
                <CardDescription>Aggregate category breakdown</CardDescription>
            </CardHeader>
            <CardContent className="flex-1 min-h-[300px] mt-4 p-6">
                {loading ? (
                    <div className="h-full w-full flex items-center justify-center text-muted-foreground text-sm">Loading chart...</div>
                ) : data.length === 0 ? (
                    <div className="h-full w-full flex items-center justify-center text-muted-foreground text-sm">No finding data available.</div>
                ) : (
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie
                                data={data}
                                cx="50%"
                                cy="50%"
                                innerRadius={65}
                                outerRadius={90}
                                paddingAngle={3}
                                dataKey="value"
                                stroke="none"
                            >
                                {data.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[entry.name] || COLORS["Unknown"]} />
                                ))}
                            </Pie>
                            <Tooltip
                                formatter={(value: any) => [`${value} findings`, 'Count']}
                                contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                            />
                            <Legend verticalAlign="bottom" height={36} iconType="circle" />
                        </PieChart>
                    </ResponsiveContainer>
                )}
            </CardContent>
        </Card>
    );
}
