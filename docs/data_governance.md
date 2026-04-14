# Data Governance Policy

**TalentMatch AI — EU AI Act Article 10 Compliance**

---

## 1. Training Data

### Current State (v1.0)

- **Type**: Synthetic training data (210 resume–job description pairs)
- **Generation**: Algorithmically created using domain-specific skill taxonomies
- **Purpose**: Initial model development and system testing
- **Bias controls**: Equal positive/negative distribution across all role categories

### Production Requirements

Before deployment with real candidate data:

1. **Consent**: Explicit opt-in consent from all data subjects
2. **Anonymization**: Remove PII (names, addresses, phone numbers) before training
3. **Representation**: Ensure balanced representation across demographic groups
4. **Audit**: Independent audit of training data for bias
5. **Documentation**: Maintain data lineage and version control

## 2. Operational Data

### Resume Processing

| Stage | Data Handling |
|---|---|
| Upload | Encrypted in transit (TLS 1.3) |
| Processing | Text extracted in memory, not persisted to disk |
| Scoring | Score and explanation stored in audit log |
| Retention | Resume text deleted after 30-day audit window |
| Archive | Anonymized metrics retained for fairness monitoring |

### Audit Log Retention

| Data | Retention Period | Purpose |
|---|---|---|
| Screening decisions | 2 years | Regulatory compliance |
| Fairness metrics | 5 years | Trend analysis |
| Model artifacts | Indefinite | Reproducibility |
| Candidate PII | 30 days | Operational + appeal window |

## 3. Data Quality

### Input Validation

- File size limit: 10 MB
- Supported formats: PDF, DOCX, TXT
- Minimum text length: 50 characters
- Encoding: UTF-8 (best-effort conversion)

### Quality Monitoring

- Track extraction success rate by file format
- Monitor for empty/garbled text extraction
- Flag resumes that produce anomalous scores
- Quarterly review of data quality metrics

## 4. Access Controls

| Role | Access Level |
|---|---|
| Candidates | Own screening results + explanation |
| HR Reviewers | Assigned candidate results + scores |
| HR Managers | Aggregate reports, override functionality |
| ML Engineers | Training data, model artifacts, evaluation metrics |
| Administrators | System configuration, audit logs |
| DPO | Full audit trail, incident reports |

## 5. Third-Party Data Sharing

| Recipient | Data Shared | Purpose | Safeguards |
|---|---|---|---|
| MLflow | Model metrics, artifacts | Experiment tracking | Self-hosted, no PII |
| Datadog | Performance metrics | System monitoring | No PII, aggregated only |
| Vigilens | Compliance evidence | Audit & governance | Encrypted, scoped access |

No candidate PII is shared with any third party.

## 6. Data Subject Rights (GDPR)

Procedures for handling data subject requests:

1. **Access request**: Respond within 30 days with all held data
2. **Rectification**: Update incorrect data within 5 business days
3. **Erasure**: Delete data within 30 days (except legal holds)
4. **Portability**: Provide data in machine-readable format (JSON)
5. **Objection**: Route to human-only review if automated processing contested

---

*Last updated: 2025-01-01*
