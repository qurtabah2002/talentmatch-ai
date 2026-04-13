"use client";

import { useEffect, useState } from "react";
import { getModelInfo, type ModelInfo } from "@/lib/api";

export default function ModelPage() {
  const [info, setInfo] = useState<ModelInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getModelInfo()
      .then(setInfo)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-[#8888a0] animate-pulse">Loading...</p>;
  if (!info) return <p className="text-danger">Could not load model info.</p>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Model Information</h1>
        <p className="mt-2 text-[#8888a0]">
          EU AI Act Art. 13 — Transparency requirements. Technical documentation
          of the AI system.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {[
          ["Model Type", info.model_type],
          ["Version", info.model_version],
          ["Status", info.is_loaded ? "✓ Loaded" : "✗ Not loaded"],
          ["Auto-Reject Threshold", `≤ ${(info.auto_reject_threshold * 100).toFixed(0)}%`],
          ["Auto-Advance Threshold", `≥ ${(info.auto_advance_threshold * 100).toFixed(0)}%`],
          [
            "Human Review Band",
            `${(info.human_review_band[0] * 100).toFixed(0)}% – ${(info.human_review_band[1] * 100).toFixed(0)}%`,
          ],
        ].map(([label, value]) => (
          <div
            key={label}
            className="flex justify-between rounded-lg border border-[#2a2a3a] bg-[#16161f] px-5 py-4"
          >
            <span className="text-sm text-[#8888a0]">{label}</span>
            <span className="text-sm font-medium">{value}</span>
          </div>
        ))}
      </div>

      {/* Compliance references */}
      <div className="rounded-xl border border-[#2a2a3a] bg-[#16161f] p-6 space-y-4">
        <h2 className="text-lg font-semibold">Compliance Framework Mapping</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[#2a2a3a] text-left text-xs text-[#8888a0]">
              <th className="pb-2">Framework</th>
              <th className="pb-2">Requirement</th>
              <th className="pb-2">Implementation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#2a2a3a]">
            {[
              ["EU AI Act Art. 9", "Risk Management", "Fairness evaluation pipeline, threshold policies"],
              ["EU AI Act Art. 10", "Data Governance", "Training data documentation, bias testing"],
              ["EU AI Act Art. 12", "Record Keeping", "Audit middleware, all decisions logged"],
              ["EU AI Act Art. 13", "Transparency", "Explanation factors, model card, score breakdown"],
              ["EU AI Act Art. 14", "Human Oversight", "Review band (20–85%), human approval required"],
              ["NIST AI RMF Map", "Context", "System classification as high-risk HR tool"],
              ["NIST AI RMF Measure", "Metrics", "Demographic parity, equal opportunity, DI ratio"],
              ["NIST AI RMF Manage", "Controls", "Threshold policies, incident response procedures"],
              ["SOC 2 CC6.1", "Access Controls", "API authentication, role-based actions"],
              ["SOC 2 CC7.2", "Monitoring", "Datadog APM, model drift detection"],
            ].map(([fw, req, impl]) => (
              <tr key={fw}>
                <td className="py-2 font-mono text-xs text-primary">{fw}</td>
                <td className="py-2">{req}</td>
                <td className="py-2 text-xs text-[#8888a0]">{impl}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
