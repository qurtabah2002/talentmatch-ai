# Data Protection Impact Assessment (DPIA)

**TalentMatch AI Resume Screening System**

*EU AI Act Art. 10 — Data and Data Governance*
*GDPR Art. 35 — Data Protection Impact Assessment*

---

## 1. System Description

TalentMatch AI processes job applicant resumes to generate compatibility scores against job descriptions. The system uses machine learning (TF-IDF + Logistic Regression) to extract text features and predict match likelihood.

### Data Processed

| Data Category | Examples | Sensitivity |
|---|---|---|
| Resume text | Skills, experience, education | Personal data |
| Job descriptions | Requirements, qualifications | Business data |
| Screening scores | 0–100 match score | Derived data |
| Explanation factors | Matched keywords, weights | Derived data |
| Audit logs | Timestamps, decisions, IDs | Operational data |

### Data NOT Processed

The model intentionally does **not** process:
- Names or demographic identifiers
- Photos or images
- Social media profiles
- Protected characteristics (age, gender, ethnicity, disability)
- Salary history

## 2. Purpose and Necessity

**Purpose**: Reduce time-to-hire by pre-screening large volumes of applications against job requirements.

**Necessity**: Manual screening of hundreds of applications per role is time-consuming and inconsistent. AI screening ensures all candidates are evaluated against the same criteria.

**Proportionality**: The system only scores text-based skill matching. It does not make final hiring decisions — human reviewers must approve all candidates in the 20–85% score band.

## 3. Risk Assessment

### High Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Bias against protected groups | Medium | High | Fairness evaluation pipeline, demographic parity testing, 80% rule validation |
| Unjustified rejection of qualified candidates | Medium | High | Human review band (20–85%), explanation factors, appeal process |
| Score manipulation via keyword stuffing | Low | Medium | TF-IDF weighting normalizes term frequency; future: semantic matching |
| Data breach of resume content | Low | High | Encryption at rest (AES-256), TLS 1.3 in transit, access controls |

### Low Risks

| Risk | Likelihood | Impact |
|---|---|---|
| System downtime | Low | Low — fallback to manual screening |
| Model staleness | Medium | Low — re-training scheduled quarterly |

## 4. Data Governance Measures

1. **Collection**: Resumes collected only with explicit applicant consent
2. **Storage**: Resume text retained only for the duration of the screening process + 30 day audit window
3. **Access**: Role-based access — only HR personnel and system administrators
4. **Deletion**: Automated purge after retention period
5. **Training data**: Synthetic data for initial model; production training uses anonymized, consented data only
6. **Cross-border**: No cross-border data transfers without adequate safeguards

## 5. Individual Rights

| Right | Implementation |
|---|---|
| **Right to explanation** | Explanation factors provided with every score (Art. 13) |
| **Right to human review** | All scores 20–85% require human decision (Art. 14) |
| **Right to contest** | Appeal process documented in human_oversight.md |
| **Right to data access** | Candidates can request their screening data |
| **Right to deletion** | Screening records deleted after retention period |
| **Right to not be subject to automated decisions** | Human oversight for all consequential decisions (GDPR Art. 22) |

## 6. Consultation

This DPIA was prepared in consultation with:
- Data Protection Officer (DPO)
- HR Department
- Engineering Team
- Legal/Compliance Team

## 7. Review Schedule

This DPIA is reviewed:
- Annually
- After any model re-training
- After significant changes to data processing
- After any bias incident

---

*Last reviewed: 2025-01-01*
*Next review due: 2025-07-01*
