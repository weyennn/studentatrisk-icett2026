# EarlyGuard — ICETT 2026

**Intelligent Two-Stage Ensemble Framework for Early Detection and Intervention of At-Risk Students**

Universitas Gadjah Mada · ICETT 2026

---

## Overview

EarlyGuard implements a two-stage prediction pipeline to identify students at risk of academic failure, balancing early detection with prediction accuracy.

| Stage | Model | Features | Objective |
|-------|-------|----------|-----------|
| 1 — Early Screening | Logistic Regression | G1 + demographics + behaviour | Maximise recall (p ≥ 0.20) |
| 2 — Confirmation | RF + XGBoost soft-voting | G1, G2, engineered features | Balanced precision & recall |

**Stage 2 Ensemble Performance:** F1 = 0.88 · Precision = 0.88 · Recall = 0.88 · ROC-AUC = 0.911

---

## Project Structure

```
earlyguard/
├── app.py                    # Streamlit entry point (multi-page)
├── train.py                  # Model training script → produces model_data.pkl
├── requirements.txt
├── .gitignore
├── README.md
│
├── config/
│   └── constants.py          # Thresholds, labels, intervention rules
│
├── pages/
│   ├── predict.py            # Main prediction dashboard
│   ├── overview.py           # Dataset statistics
│   └── about.py              # Framework, methodology & authors
│
├── utils/
│   ├── __init__.py
│   ├── model.py              # Cached model loader (with error handling)
│   ├── prediction.py         # Feature engineering + two-stage inference
│   └── style.py              # Global CSS injection
│
├── assets/
│   └── logo.svg              # App logo (used as page icon)
│
└── data/
```

> **Note:** `model_data.pkl` and `student-mat.csv` are excluded from version control (see `.gitignore`).
> Follow the **Quick Start** steps below before running the app.

---

## Quick Start

### Prerequisites

- Python >= 3.10
- UCI Student Performance dataset (`student-mat.csv`)

### 1 — Install dependencies

```bash
pip install -r requirements.txt
```

### 2 — Download the dataset

Download from the UCI Machine Learning Repository and place `student-mat.csv` in the project root:

```
https://archive.ics.uci.edu/dataset/320/student+performance
```

### 3 — Train the model

```bash
python train.py
```

This produces `model_data.pkl` in the project root. Optional arguments:

```bash
python train.py --data path/to/student-mat.csv   # custom data path
python train.py --output path/to/model_data.pkl  # custom output path
```

### 4 — Run the app

```bash
streamlit run app.py
```

---

## model_data.pkl — Key Reference

The training script saves a single pickle file containing all artefacts required by the app.

| Key | Type | Description |
|-----|------|-------------|
| `lr_model` | `LogisticRegression` | Stage 1 classifier |
| `rf_model` | `RandomForestClassifier` | Stage 2 ensemble member |
| `xgb_model` | `XGBClassifier` | Stage 2 ensemble member |
| `le_dict` | `dict[str, LabelEncoder]` | One encoder per categorical column |
| `cat_cols` | `list[str]` | Column names that were label-encoded |
| `stage1_features` | `list[str]` | Feature list for Stage 1 inference |
| `stage2_features` | `list[str]` | Feature list for Stage 2 inference |
| `stage1_threshold` | `float` | Classification threshold for Stage 1 (0.20) |
| `feature_importance` | `dict[str, float]` | Ensemble-averaged importance, sums to 1 |

---

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Set `app.py` as the main file
4. Upload `model_data.pkl` and `student-mat.csv` to the repo (they are gitignored by default — either remove the gitignore entries or upload via Streamlit Secrets / a private branch)
5. Deploy

---

## Dataset

UCI Student Performance Dataset — Mathematics subject, 395 students, Portuguese secondary school.
Source: https://archive.ics.uci.edu/dataset/320/student+performance

---

## Intervention Mapping (from Paper — Table III)

| Rank | Feature | Importance | Recommended Intervention |
|------|---------|------------|--------------------------|
| 1 | G2 (Second term grade) | 0.324 | Academic tutoring and additional practice |
| 2 | Absences | 0.186 | Attendance counseling and monitoring |
| 3 | Failures (prior) | 0.142 | Remedial coursework and mentoring |
| 4 | Grade trend (G2−G1) | 0.118 | Academic advising and study skills support |
| 5 | G1 (First term grade) | 0.095 | General academic monitoring |

---

## Authors

| Name | Affiliation |
|------|------------|
| Yayang Matira *(corresponding)* | Dept. of Computer Science and Electronics, UGM |
| Maulana Ihsan Ahmad | Dept. of Computer Science and Electronics, UGM |
| Guntur Budi Herwanto | Dept. of Computer Science and Electronics, UGM |
| Fadel Muhamad | Dept. of Indonesian Language and Literature Education, UNY |

---

## Acknowledgement

This work was supported by the Indonesian Endowment Fund for Education (LPDP), Ministry of Education, Culture, Research, and Technology of the Republic of Indonesia.
