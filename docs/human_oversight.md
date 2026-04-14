# Human Oversight Procedures

**TalentMatch AI — EU AI Act Article 14 Compliance**

---

## 1. Overview

TalentMatch AI implements a human-in-the-loop (HITL) design for all consequential hiring decisions. This document defines the procedures for human oversight of automated screening decisions.

## 2. Decision Framework

### Score Bands and Required Actions

| Score Range | Action | Human Required | SLA |
|---|---|---|---|
| 0–20 | Auto-reject | No (logged + auditable) | Notification within 24h |
| 20–85 | Human review | **Yes — mandatory** | Decision within 48h |
| 85–100 | Auto-advance | No (spot-check required) | Advance within 24h |

### Human Review Process

```
Candidate submits resume
        │
        ▼
   AI Screening (automated)
        │
        ├── Score ≤ 20 ──────► Auto-reject (logged)
        │                         │
        │                         ▼
        │                    Candidate notified
        │                    with explanation
        │
        ├── Score 20–85 ─────► Human Review Queue
        │                         │
        │                         ▼
        │                    HR Reviewer sees:
        │                    • AI score + explanation
        │                    • Full resume
        │                    • Job requirements
        │                    • Fairness flags
        │                         │
        │                    ┌────┴────┐
        │                    ▼         ▼
        │                  Approve   Reject
        │                    │         │
        │                    ▼         ▼
        │               Advance    Notify with
        │               to next    explanation
        │               stage
        │
        └── Score ≥ 85 ──────► Auto-advance (logged)
                                  │
                                  ▼
                             Subject to 10%
                             spot-check audit
```

## 3. Reviewer Qualifications

Human reviewers must:
- Be qualified HR professionals
- Complete bias awareness training (minimum annually)
- Understand the AI system's capabilities and limitations (model card review)
- Not be solely reliant on the AI recommendation — independent judgment required

## 4. Override Authority

Reviewers have **full override authority**:
- Can advance candidates the AI rejected
- Can reject candidates the AI advanced
- All overrides are logged with justification
- Override patterns are monitored for consistency

## 5. Appeal Process

Candidates may appeal any automated decision:

1. **Submit appeal** via the application portal within 14 days
2. **Human review**: A different reviewer (not the original) evaluates the appeal
3. **Response**: Decision communicated within 5 business days
4. **Escalation**: If unsatisfied, candidate may escalate to the DPO

## 6. Monitoring

- Weekly report: auto-reject rate, human review rate, auto-advance rate
- Monthly review: override frequency, appeal outcomes, fairness drift
- Quarterly audit: spot-check of auto-advance decisions (10% sample)

## 7. Emergency Stop

If systemic bias is detected:
1. Halt all automated decisions immediately
2. Route 100% of candidates to human review
3. Trigger incident response procedure (see incident_response.md)
4. Notify DPO and affected candidates

---

*Last updated: 2025-01-01*
