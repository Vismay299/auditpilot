import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface StatsCardProps {
    title: string;
    value: string | number;
    icon: LucideIcon;
    description?: string;
    trend?: string;
    trendUp?: boolean;
}

export function StatsCard({ title, value, icon: Icon, description, trend, trendUp }: StatsCardProps) {
    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
                <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{value}</div>
                {(description || trend) && (
                    <p className="text-xs text-muted-foreground mt-1">
                        {trend && (
                            <span className={trendUp ? "text-green-500 font-medium" : "text-red-500 font-medium"}>
                                {trend}
                            </span>
                        )}
                        {" "}{description}
                    </p>
                )}
            </CardContent>
        </Card>
    );
}
