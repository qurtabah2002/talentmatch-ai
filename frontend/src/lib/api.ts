const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001/api";

export interface ScreeningResult {
  screening_id: string;
  timestamp: string;
  candidate_id: string;
  job_title: string;
  score: number;
  score_raw: number;
  model_version: string;
  explanation: { term: string; weight: number; in_resume: boolean; in_job: boolean }[];
  action: "auto_reject" | "human_review" | "auto_advance";
  requires_human_review: boolean;
  confidence: string;
  action_reason: string;
  fairness_flags: string[];
}

export interface FairnessReport {
  model_version: string;
  generated_at: string;
  demographic_parity: Record<string, Record<string, number>>;
  equal_opportunity: Record<string, Record<string, number>>;
  disparate_impact_ratio: number;
  recommendation: string;
}

export interface ModelInfo {
  model_version: string;
  model_type: string;
  is_loaded: boolean;
  auto_reject_threshold: number;
  auto_advance_threshold: number;
  human_review_band: number[];
  fairness_metrics_url: string;
}

export async function screenResume(
  resumeText: string,
  jobDescription: string,
  jobTitle?: string,
  candidateId?: string,
): Promise<ScreeningResult> {
  const res = await fetch(`${API_BASE}/screen`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
      job_title: jobTitle || "Unspecified Position",
      candidate_id: candidateId || undefined,
    }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function screenResumeFile(
  file: File,
  jobDescription: string,
  jobTitle?: string,
  candidateId?: string,
): Promise<ScreeningResult> {
  const form = new FormData();
  form.append("file", file);
  form.append("job_description", jobDescription);
  if (jobTitle) form.append("job_title", jobTitle);
  if (candidateId) form.append("candidate_id", candidateId);

  const res = await fetch(`${API_BASE}/screen/upload`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getFairnessReport(): Promise<FairnessReport> {
  const res = await fetch(`${API_BASE}/model/fairness`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getModelInfo(): Promise<ModelInfo> {
  const res = await fetch(`${API_BASE}/model/info`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
