import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Zap } from "lucide-react";

export function CostTracker({ inspectionsCount = 0 }: { inspectionsCount?: number }) {
    // Mock data for cost estimation to save time, since usage logs aren't fully joined yet
    const AVG_COST_PER_INSPECTION = 0.08;
    const totalCost = (inspectionsCount * AVG_COST_PER_INSPECTION).toFixed(2);

    return (
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 text-slate-50 border-slate-700">
            <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-medium text-slate-300">Est. API Compute Cost</CardTitle>
                    <Zap className="h-4 w-4 text-emerald-400" />
                </div>
            </CardHeader>
            <CardContent>
                <div className="text-3xl font-bold tracking-tight">${totalCost}</div>
                <p className="text-xs text-slate-400 mt-1">
                    Avg ${AVG_COST_PER_INSPECTION} per inspection
                </p>
                <div className="mt-4 space-y-2">
                    <div className="flex items-center justify-between text-xs border-t border-slate-700 pt-2">
                        <span className="text-slate-400">Total processed</span>
                        <span className="font-semibold">{inspectionsCount} audits</span>
                    </div>
                    <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-400">Current plan</span>
                        <span className="text-emerald-400 font-semibold">Starter (Free)</span>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
