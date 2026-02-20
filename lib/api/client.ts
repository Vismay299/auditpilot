import { createClient } from '@/lib/supabase/client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthToken(): Promise<string | null> {
  const supabase = createClient();
  const { data: { session } } = await supabase.auth.getSession();
  return session?.access_token || null;
}

async function headers(): Promise<HeadersInit> {
  const h: Record<string, string> = {
    "Content-Type": "application/json",
  };
  const token = await getAuthToken();
  console.log("Client API injecting token:", token ? "PRESENT" : "MISSING")
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}


export type Inspection = {
  id: string;
  name: string;
  status: string;
  org_id: string;
  site_location: string | null;
  site_address: string | null;
  total_files: number;
  total_findings: number;
  risk_level: string | null;
  report_narrative: string | null;
};

export type Finding = {
  id: string;
  file_id: string | null;
  category: string;
  severity: string | null;
  confidence_score: number | null;
  needs_review: boolean;
  description: string | null;
  ai_caption: string | null;
  transcription: string | null;
  location_code: string | null;
  equipment_id: string | null;
  created_at: string | null;
};

export type InspectionCreate = {
  name: string;
  site_location?: string | null;
  site_address?: string | null;
};

export type FileRecord = {
  id: string;
  file_name: string;
  file_type: string;
  status: string;
  file_size: number | null;
  created_at: string | null;
};

export const api = {
  async listInspections(): Promise<Inspection[]> {
    const res = await fetch(`${API_URL}/inspections`, { headers: await headers() });
    if (!res.ok) {
      const text = await res.text();
      try {
        throw new Error(JSON.parse(text).detail || text);
      } catch {
        throw new Error(text);
      }
    }
    return res.json();
  },

  async getInspection(id: string): Promise<Inspection> {
    const res = await fetch(`${API_URL}/inspections/${id}`, { headers: await headers() });
    if (!res.ok) {
      const text = await res.text();
      try { throw new Error(JSON.parse(text).detail || text); } catch { throw new Error(text); }
    }
    return res.json();
  },

  async createInspection(data: InspectionCreate): Promise<Inspection> {
    const res = await fetch(`${API_URL}/inspections`, {
      method: "POST",
      headers: await headers(),
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const text = await res.text();
      try { throw new Error(JSON.parse(text).detail || text); } catch { throw new Error(text); }
    }
    return res.json();
  },

  async listFiles(inspectionId: string): Promise<{ files: FileRecord[] }> {
    const res = await fetch(`${API_URL}/inspections/${inspectionId}/files`, {
      headers: await headers(),
    });
    if (!res.ok) {
      const text = await res.text();
      try { throw new Error(JSON.parse(text).detail || text); } catch { throw new Error(text); }
    }
    return res.json();
  },

  async uploadFiles(
    inspectionId: string,
    files: File[],
    onProgress?: (loaded: number, total: number) => void
  ): Promise<{ files: { id: string; file_name: string; status: string }[] }> {
    const token = await getAuthToken();
    const form = new FormData();
    files.forEach((f) => form.append("files", f));

    const xhr = new XMLHttpRequest();
    return new Promise((resolve, reject) => {
      xhr.upload.addEventListener("progress", (e) => {
        if (e.lengthComputable && onProgress) onProgress(e.loaded, e.total);
      });
      xhr.addEventListener("load", () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            resolve(JSON.parse(xhr.responseText));
          } catch {
            reject(new Error("Invalid response"));
          }
        } else {
          reject(new Error(xhr.responseText || `Upload failed ${xhr.status}`));
        }
      });
      xhr.addEventListener("error", () => reject(new Error("Network error")));
      xhr.open("POST", `${API_URL}/inspections/${inspectionId}/files`);
      if (token) xhr.setRequestHeader("Authorization", `Bearer ${token}`);
      xhr.send(form);
    });
  },

  async listFindings(inspectionId: string): Promise<{ findings: Finding[] }> {
    const res = await fetch(`${API_URL}/inspections/${inspectionId}/findings`, {
      headers: await headers(),
    });
    if (!res.ok) {
      const text = await res.text();
      try { throw new Error(JSON.parse(text).detail || text); } catch { throw new Error(text); }
    }
    return res.json();
  },

  async getInspectionStats(): Promise<{
    totalInspections: number;
    totalFindings: number;
    pendingReviews: number;
    avgProcessingTime: string;
  }> {
    const res = await fetch(`${API_URL}/inspections/stats`, { headers: await headers() });
    if (!res.ok) {
      const text = await res.text();
      try { throw new Error(JSON.parse(text).detail || text); } catch { throw new Error(text); }
    }
    return res.json();
  },

  async getFindingsStats(): Promise<{ name: string; value: number }[]> {
    const res = await fetch(`${API_URL}/findings/stats`, { headers: await headers() });
    if (!res.ok) {
      const text = await res.text();
      try { throw new Error(JSON.parse(text).detail || text); } catch { throw new Error(text); }
    }
    return res.json();
  },

  async getReviewQueue(): Promise<(Finding & { inspection: { id: string; name: string } })[]> {
    const res = await fetch(`${API_URL}/findings/review-queue`, { headers: await headers() });
    if (!res.ok) {
      const text = await res.text();
      try { throw new Error(JSON.parse(text).detail || text); } catch { throw new Error(text); }
    }
    return res.json();
  }
};
