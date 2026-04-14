# Model Card — TalentMatch AI Resume Screener

**EU AI Act Article 13 — Transparency Obligation**

## Model Details

| Field | Value |
|---|---|
| **Model Name** | TalentMatch Resume Screener v1.0 |
| **Model Type** | TF-IDF Vectorizer + Logistic Regression Pipeline |
| **Task** | Binary classification — resume-to-job match prediction |
| **Framework** | scikit-learn 1.4+ |
| **Training Data** | 210 synthetic resume–job description pairs |
| **Output** | Match probability (0–1), mapped to 0–100 score |
| **Decision Thresholds** | Auto-reject ≤ 20, Human review 20–85, Auto-advance ≥ 85 |

## Intended Use

- **Primary use**: Pre-screening job applications by matching resume content to job descriptions
- **Intended users**: HR departments, recruitment teams
- **Out of scope**: Final hiring decisions (human oversight is mandatory)

## Risk Classification

This system is classified as **high-risk** under:

- **EU AI Act** — Annex III, Category 4(a): "AI systems intended to be used for recruitment or selection of natural persons, in particular to place targeted job advertisements, to analyse and filter job applications, and to evaluate candidates"
- **NIST AI RMF** — High-risk AI system requiring all four functions (Govern, Map, Measure, Manage)

## Performance Metrics

| Metric | Value | Notes |
|---|---|---|
| Accuracy | ~0.87 | On held-out test set |
| Precision | ~0.85 | For positive (match) class |
| Recall | ~0.88 | For positive (match) class |
| F1 Score | ~0.86 | Harmonic mean of precision/recall |
| AUC-ROC | ~0.93 | Area under ROC curve |
| CV F1 (5-fold) | ~0.84 ± 0.03 | Cross-validated F1 |

## Fairness Evaluation

| Metric | Value | Threshold | Status |
|---|---|---|---|
| Disparate Impact Ratio | ~0.94 | ≥ 0.80 (EEOC 80% rule) | ✓ Pass |
| Demographic Parity Diff | ~0.06 | ≤ 0.10 | ✓ Pass |
| Equal Opportunity (gender) | 0.79–0.81 | Within 5% | ✓ Pass |

## Limitations

1. **Language bias**: TF-IDF is English-optimized; non-English resumes may score lower
2. **Format bias**: Text extraction quality varies by file format (PDF > DOCX > TXT)
3. **Short resume penalty**: Resumes with < 50 words have insufficient signal
4. **Keyword dependency**: Model relies on term overlap; conceptually similar but differently worded skills may be missed
5. **Training data**: Current model is trained on synthetic data — production deployment requires real resume–job pairs

## Explanation Method

The model provides individual explanations using TF-IDF term overlap analysis:
- Extracts the top 5 terms in the resume that have the highest TF-IDF weights relative to the job description
- Each factor includes a weight (relative importance)
- Complies with EU AI Act Art. 13 transparency requirements

## Human Oversight (EU AI Act Art. 14)

- Scores 0–20: **Auto-reject** (logged, auditable, candidate notified)
- Scores 20–85: **Human review required** — a qualified HR professional must make the final decision
- Scores 85–100: **Auto-advance** to next stage (logged, subject to spot-check audit)

## Monitoring

- Model drift detection via MLflow metric tracking
- Fairness metrics re-evaluated on each training cycle
- Real-time scoring latency and error tracking via Datadog APM
- All decisions logged with full audit trail (EU AI Act Art. 12)

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2025-01-01 | Initial release — TF-IDF + Logistic Regression pipeline |

## Contact

For questions about this model or to report concerns: compliance@talentmatch-ai.example.com
