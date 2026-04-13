"use client";

import { useEffect, useState } from "react";
import { getFairnessReport, type FairnessReport } from "@/lib/api";

function BarChart({
  data,
  label,
}: {
  data: Record<string, number>;
  label: string;
}) {
  return (
    <div className="space-y-2">
      <h4 className="text-sm font-medium text-[#8888a0]">{label}</h4>
      {Object.entries(data).map(([group, value]) => (
        <div key={group} className="flex items-center gap-3">
          <span className="w-20 text-right text-xs text-[#8888a0] capitalize">
            {group.replace(/_/g, " ")}
          </span>
          <div className="flex-1 h-5 rounded bg-[#0a0a0f] overflow-hidden">
            <div
              className="h-full rounded bg-primary transition-all duration-700"
              style={{ width: `${value * 100}%` }}
            />
          </div>
          <span className="w-12 text-xs font-mono">{(value * 100).toFixed(1)}%</span>
        </div>
      ))}
    </div>
  );
}

export default function DashboardPage() {
  const [report, setReport] = useState<FairnessReport | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFairnessReport()
      .then(setReport)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-[#8888a0] animate-pulse">Loading fairness metrics...</p>;
  }

  if (error) {
    return (
      <div className="rounded-lg border border-danger/30 bg-danger/10 p-4 text-sm text-danger">
        Failed to load fairness data: {error}
      </div>
    );
  }

  if (!report) return null;

  const dirColor =
    report.disparate_impact_ratio >= 0.8 ? "text-green-400" : "text-red-400";

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Fairness Dashboard</h1>
        <p className="mt-2 text-[#8888a0]">
          NIST AI RMF — Measure function. Continuous fairness monitoring across
          demographic groups.
        </p>
      </div>

      {/* Key metric */}
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-5 text-center">
          <p className="text-xs text-[#8888a0]">Disparate Impact Ratio</p>
          <p className={`mt-1 text-3xl font-bold ${dirColor}`}>
            {report.disparate_impact_ratio.toFixed(2)}
          </p>
          <p className="text-xs text-[#8888a0] mt-1">
            {report.disparate_impact_ratio >= 0.8 ? "✓ Passes 80% rule" : "✗ Below 80% threshold"}
          </p>
        </div>
        <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-5 text-center">
          <p className="text-xs text-[#8888a0]">Model Version</p>
          <p className="mt-1 text-lg font-mono">{report.model_version}</p>
        </div>
        <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-5 text-center">
          <p className="text-xs text-[#8888a0]">Last Evaluated</p>
          <p className="mt-1 text-lg">
            {new Date(report.generated_at).toLocaleDateString()}
          </p>
        </div>
      </div>

      {/* Demographic Parity */}
      <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-6 space-y-6">
        <h2 className="text-lg font-semibold">Demographic Parity</h2>
        <p className="text-xs text-[#8888a0]">
          P(Ŷ=1 | group=g) — Positive prediction rate should be similar across groups.
        </p>
        {Object.entries(report.demographic_parity).map(([attr, data]) => (
          <BarChart key={attr} data={data} label={attr.replace(/_/g, " ")} />
        ))}
      </div>

      {/* Equal Opportunity */}
      <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-6 space-y-6">
        <h2 className="text-lg font-semibold">Equal Opportunity</h2>
        <p className="text-xs text-[#8888a0]">
          P(Ŷ=1 | Y=1, group=g) — True positive rate for qualified candidates.
        </p>
        {Object.entries(report.equal_opportunity).map(([attr, data]) => (
          <BarChart key={attr} data={data} label={attr.replace(/_/g, " ")} />
        ))}
      </div>

      {/* Recommendation */}
      <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-6">
        <h2 className="text-lg font-semibold mb-2">Recommendation</h2>
        <p className="text-sm text-[#8888a0]">{report.recommendation}</p>
      </div>
    </div>
  );
}
