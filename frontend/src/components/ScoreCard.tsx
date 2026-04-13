import type { ScreeningResult } from "@/lib/api";

interface Factor {
  term: string;
  weight: number;
  in_resume: boolean;
  in_job: boolean;
}

const ACTION_STYLES = {
  auto_reject: { bg: "bg-red-500/10", border: "border-red-500/30", text: "text-red-400", label: "Auto-Reject" },
  human_review: { bg: "bg-yellow-500/10", border: "border-yellow-500/30", text: "text-yellow-400", label: "Human Review Required" },
  auto_advance: { bg: "bg-green-500/10", border: "border-green-500/30", text: "text-green-400", label: "Auto-Advance" },
};

export default function ScoreCard({ result }: { result: ScreeningResult }) {
  const style = ACTION_STYLES[result.action];
  const circumference = 2 * Math.PI * 45;
  const offset = circumference - (result.score / 100) * circumference;

  const scoreColor =
    result.score >= 70 ? "#10b981" : result.score >= 40 ? "#f59e0b" : "#ef4444";

  return (
    <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-6 space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-xl font-bold">Screening Result</h2>
          <p className="text-xs text-[#8888a0] mt-1">
            ID: {result.screening_id} · {result.job_title}
          </p>
        </div>
        <span className={`rounded-full px-3 py-1 text-xs font-medium ${style.bg} ${style.border} ${style.text} border`}>
          {style.label}
        </span>
      </div>

      <div className="flex items-center gap-8">
        {/* Score ring */}
        <div className="relative flex-shrink-0">
          <svg width="110" height="110" viewBox="0 0 110 110">
            <circle cx="55" cy="55" r="45" fill="none" stroke="#2a2a3a" strokeWidth="8" />
            <circle
              cx="55" cy="55" r="45" fill="none"
              stroke={scoreColor}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              transform="rotate(-90 55 55)"
              className="score-ring"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-bold" style={{ color: scoreColor }}>
              {Math.round(result.score)}
            </span>
            <span className="text-[10px] text-[#8888a0]">/ 100</span>
          </div>
        </div>

        {/* Details */}
        <div className="space-y-2 text-sm">
          <div className="flex gap-4">
            <span className="text-[#8888a0]">Confidence:</span>
            <span className="capitalize">{result.confidence}</span>
          </div>
          <div className="flex gap-4">
            <span className="text-[#8888a0]">Model:</span>
            <span className="font-mono text-xs">{result.model_version}</span>
          </div>
          <div className="flex gap-4">
            <span className="text-[#8888a0]">Candidate:</span>
            <span>{result.candidate_id}</span>
          </div>
          <p className="text-xs text-[#8888a0] italic">{result.action_reason}</p>
        </div>
      </div>

      {/* Human oversight banner */}
      {result.requires_human_review && (
        <div className="rounded-lg border border-yellow-500/30 bg-yellow-500/10 px-4 py-3 text-sm">
          <p className="font-medium text-yellow-400">⚠ Human Review Required</p>
          <p className="mt-1 text-xs text-yellow-200/70">
            EU AI Act Art. 14 — This candidate's score falls in the human review band.
            A human decision-maker must approve or reject before proceeding.
          </p>
        </div>
      )}

      {/* Explanation factors */}
      {result.explanation.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-[#8888a0] mb-2">Explanation Factors</h3>
          <div className="flex flex-wrap gap-2">
            {(result.explanation as Factor[]).map((f) => (
              <span
                key={f.term}
                className="inline-flex items-center gap-1 rounded bg-primary/10 px-2 py-1 text-xs text-primary"
              >
                {f.term}
                <span className="text-[10px] text-primary/60">
                  {(f.weight * 100).toFixed(0)}%
                </span>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Fairness flags */}
      {result.fairness_flags.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-[#8888a0] mb-1">Fairness Flags</h3>
          <ul className="space-y-1">
            {result.fairness_flags.map((flag) => (
              <li key={flag} className="text-xs text-yellow-400">
                ⚡ {flag.replace(/_/g, " ")}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Audit trail */}
      <div className="border-t border-[#2a2a3a] pt-4 text-[10px] text-[#555] font-mono">
        Screening ID: {result.screening_id} | Timestamp: {result.timestamp} | Model: {result.model_version}
      </div>
    </div>
  );
}
