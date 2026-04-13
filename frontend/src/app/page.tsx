"use client";

import { useState } from "react";
import { screenResume, screenResumeFile, type ScreeningResult } from "@/lib/api";
import ScoreCard from "@/components/ScoreCard";

const SAMPLE_JOBS = [
  {
    title: "Senior Data Scientist",
    description:
      "We are looking for a Senior Data Scientist with 5+ years of experience in machine learning, Python, TensorFlow/PyTorch, and statistical modeling. Experience with NLP, computer vision, and deploying models to production is required. Strong communication skills and ability to work cross-functionally.",
  },
  {
    title: "Backend Engineer",
    description:
      "Seeking a Backend Engineer proficient in Java/Spring Boot, microservices architecture, AWS, Docker, and Kubernetes. Must have experience with PostgreSQL, Redis, REST APIs, and CI/CD pipelines. 3+ years of professional experience.",
  },
  {
    title: "ML Engineer",
    description:
      "ML Engineer role requiring Python, scikit-learn, MLflow, feature engineering, and model deployment experience. Must be comfortable with Docker, Spark, and production ML systems. Experience with fairness testing and model monitoring preferred.",
  },
];

export default function HomePage() {
  const [mode, setMode] = useState<"text" | "file">("text");
  const [resumeText, setResumeText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [jobIndex, setJobIndex] = useState(0);
  const [customJob, setCustomJob] = useState("");
  const [candidateId, setCandidateId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ScreeningResult | null>(null);

  const selectedJob = SAMPLE_JOBS[jobIndex];
  const jobDesc = customJob || selectedJob.description;
  const jobTitle = customJob ? "Custom Position" : selectedJob.title;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      let res: ScreeningResult;
      if (mode === "file" && file) {
        res = await screenResumeFile(file, jobDesc, jobTitle, candidateId || undefined);
      } else {
        res = await screenResume(resumeText, jobDesc, jobTitle, candidateId || undefined);
      }
      setResult(res);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Screening failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Screen a Resume</h1>
        <p className="mt-2 text-[#8888a0]">
          Upload or paste a resume to evaluate against a job description.
          Scores between 20–85 require human review (EU AI Act Art. 14).
        </p>
      </div>

      <form onSubmit={handleSubmit} className="grid gap-6 lg:grid-cols-2">
        {/* Left — Resume input */}
        <div className="space-y-4">
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => setMode("text")}
              className={`rounded px-3 py-1.5 text-sm font-medium transition ${
                mode === "text"
                  ? "bg-primary text-white"
                  : "bg-[#16161f] text-[#8888a0] hover:text-white"
              }`}
            >
              Paste Text
            </button>
            <button
              type="button"
              onClick={() => setMode("file")}
              className={`rounded px-3 py-1.5 text-sm font-medium transition ${
                mode === "file"
                  ? "bg-primary text-white"
                  : "bg-[#16161f] text-[#8888a0] hover:text-white"
              }`}
            >
              Upload File
            </button>
          </div>

          {mode === "text" ? (
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste resume text here..."
              rows={12}
              className="w-full rounded-lg border border-[#2a2a3a] bg-[#16161f] px-4 py-3 text-sm placeholder:text-[#555] focus:border-primary focus:outline-none"
              required={mode === "text"}
            />
          ) : (
            <div className="flex h-48 items-center justify-center rounded-lg border-2 border-dashed border-[#2a2a3a] bg-[#16161f]">
              <label className="cursor-pointer text-center">
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  className="hidden"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                />
                {file ? (
                  <p className="text-sm">{file.name}</p>
                ) : (
                  <>
                    <p className="text-lg">📄</p>
                    <p className="text-sm text-[#8888a0]">
                      Drop PDF, DOCX, or TXT file here
                    </p>
                  </>
                )}
              </label>
            </div>
          )}

          <input
            type="text"
            value={candidateId}
            onChange={(e) => setCandidateId(e.target.value)}
            placeholder="Candidate ID (optional)"
            className="w-full rounded-lg border border-[#2a2a3a] bg-[#16161f] px-4 py-2 text-sm placeholder:text-[#555] focus:border-primary focus:outline-none"
          />
        </div>

        {/* Right — Job description */}
        <div className="space-y-4">
          <label className="text-sm font-medium text-[#8888a0]">Job Description</label>

          <div className="flex flex-wrap gap-2">
            {SAMPLE_JOBS.map((j, i) => (
              <button
                key={j.title}
                type="button"
                onClick={() => {
                  setJobIndex(i);
                  setCustomJob("");
                }}
                className={`rounded px-3 py-1 text-xs font-medium transition ${
                  jobIndex === i && !customJob
                    ? "bg-primary/20 text-primary ring-1 ring-primary"
                    : "bg-[#16161f] text-[#8888a0] hover:text-white"
                }`}
              >
                {j.title}
              </button>
            ))}
          </div>

          <textarea
            value={customJob || selectedJob.description}
            onChange={(e) => setCustomJob(e.target.value)}
            rows={10}
            className="w-full rounded-lg border border-[#2a2a3a] bg-[#16161f] px-4 py-3 text-sm placeholder:text-[#555] focus:border-primary focus:outline-none"
          />

          <button
            type="submit"
            disabled={loading || (mode === "text" ? !resumeText.trim() : !file)}
            className="w-full rounded-lg bg-primary py-3 font-semibold text-white transition hover:bg-primary-dark disabled:opacity-50"
          >
            {loading ? "Screening..." : "Screen Resume"}
          </button>
        </div>
      </form>

      {error && (
        <div className="rounded-lg border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
          {error}
        </div>
      )}

      {result && <ScoreCard result={result} />}
    </div>
  );
}
