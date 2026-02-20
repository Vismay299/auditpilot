import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full text-center space-y-6">
        <h1 className="text-4xl font-bold">AuditPilot</h1>
        <p className="text-lg text-muted-foreground">
          Automated inspection report generation
        </p>
        <Button asChild size="lg">
          <Link href="/dashboard">Go to dashboard</Link>
        </Button>
      </div>
    </main>
  );
}
