# Incident Response Plan — Bias & Fairness Incidents

**TalentMatch AI — NIST AI RMF Manage Function**

---

## 1. Scope

This plan covers incidents related to:
- Detected bias in model predictions
- Disparate impact ratio falling below 0.80
- Complaint from a candidate about unfair treatment
- Model drift causing score distribution changes
- Data quality issues affecting fairness

## 2. Severity Levels

| Level | Criteria | Response Time | Example |
|---|---|---|---|
| **P1 — Critical** | Active harm to candidates | 1 hour | Disparate impact < 0.60 |
| **P2 — High** | Likely harm, needs investigation | 4 hours | DI ratio 0.60–0.80, pattern of complaints |
| **P3 — Medium** | Potential concern, monitoring needed | 24 hours | DI ratio nearing threshold, single complaint |
| **P4 — Low** | Minor drift, no immediate harm | 1 week | Metric drift within acceptable bounds |

## 3. Response Procedures

### P1 — Critical

1. **Immediate**: Activate emergency stop — halt all automated screening
2. **Notify**: DPO, CISO, HR Director within 1 hour
3. **Investigate**: Identify root cause (data issue, model drift, or code bug)
4. **Remediate**: Fix issue, retrain model if needed
5. **Validate**: Run full fairness evaluation before resuming
6. **Communicate**: Notify affected candidates within 72 hours
7. **Document**: Full incident report for regulatory file

### P2 — High

1. **Route**: Move all decisions to human review queue
2. **Investigate**: Identify scope and root cause within 4 hours
3. **Fix**: Deploy fix to staging, validate fairness
4. **Monitor**: Enhanced monitoring for 7 days post-fix
5. **Document**: Incident report within 48 hours

### P3 — Medium

1. **Monitor**: Increase monitoring frequency
2. **Investigate**: Root cause analysis within 24 hours
3. **Plan**: Schedule remediation if confirmed
4. **Review**: Verify in next fairness evaluation cycle

### P4 — Low

1. **Log**: Record observation
2. **Track**: Add to next model review agenda
3. **Monitor**: Standard monitoring continues

## 4. Root Cause Categories

| Category | Investigation Steps |
|---|---|
| **Training data bias** | Audit data distribution, check for underrepresented groups |
| **Feature drift** | Compare current input distribution to training distribution |
| **Code regression** | Review recent deployments, check preprocessing changes |
| **Threshold misconfiguration** | Verify decision thresholds match policy |
| **External factors** | Check for changes in applicant demographics or job market |

## 5. Communication Templates

### To affected candidates (P1/P2):

> We identified a technical issue with our automated screening system that may have affected your application. We are re-evaluating all affected applications with human reviewers. You will receive an updated decision within [X] business days. We apologize for any inconvenience.

### To regulator (if required):

> In accordance with [EU AI Act / local regulations], we are reporting the following incident involving our high-risk AI system used in recruitment...

## 6. Post-Incident Review

Within 2 weeks of resolution:
1. **Timeline**: Document full incident timeline
2. **Root cause**: Confirmed root cause and contributing factors
3. **Impact**: Number of affected candidates and decisions
4. **Fix**: What was changed and how it was validated
5. **Prevention**: What systemic changes prevent recurrence
6. **Monitoring**: What new checks or alerts were added

## 7. Contact List

| Role | Responsibility |
|---|---|
| On-call Engineer | First responder, emergency stop authority |
| ML Team Lead | Model investigation, retraining |
| DPO | Regulatory notification, candidate communication |
| HR Director | Human review escalation, candidate appeals |
| CISO | Data security aspects, access review |

---

*Last updated: 2025-01-01*
*Next drill: 2025-04-01*
