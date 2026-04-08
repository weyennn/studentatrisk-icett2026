"""
train.py
--------
EarlyGuard — Model training script.

Trains the two-stage prediction pipeline and saves all artefacts to
`model_data.pkl` in the project root.

Usage:
    python train.py
    python train.py --data path/to/student-mat.csv
    python train.py --output path/to/model_data.pkl

Expected output keys in model_data.pkl:
    lr_model            : sklearn LogisticRegression  (Stage 1)
    rf_model            : sklearn RandomForestClassifier (Stage 2)
    xgb_model           : xgboost XGBClassifier (Stage 2)
    le_dict             : dict[col_name -> LabelEncoder]
    cat_cols            : list[str]  — columns that were label-encoded
    stage1_features     : list[str]  — feature names used by Stage 1
    stage2_features     : list[str]  — feature names used by Stage 2
    stage1_threshold    : float      — classification threshold for Stage 1 (0.20)
    feature_importance  : dict[str -> float]  — Stage 2 ensemble importances
"""

import argparse
import os
import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

# ── Constants ──────────────────────────────────────────────────────────────────

STAGE1_THRESHOLD = 0.20   # Low threshold → maximise recall at Stage 1

STAGE1_FEATURES = [
    "G1", "sex", "age", "address", "famsize", "Pstatus",
    "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian",
    "traveltime", "studytime", "failures", "schoolsup", "famsup",
    "paid", "activities", "nursery", "higher", "internet",
    "romantic", "famrel", "freetime", "goout", "Dalc", "Walc",
    "health", "absences", "parent_edu", "support_total",
]

STAGE2_FEATURES = STAGE1_FEATURES + ["G2", "grade_trend"]

CATEGORICAL_COLS = [
    "sex", "address", "famsize", "Pstatus",
    "Mjob", "Fjob", "reason", "guardian",
    "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic",
]

# ── Data loading & preprocessing ───────────────────────────────────────────────

def load_and_prepare(data_path: str) -> pd.DataFrame:
    """Load the UCI dataset and engineer features."""
    df = pd.read_csv(data_path, sep=";")

    # Target: G3 < 10 → at risk
    df["at_risk"] = (df["G3"] < 10).astype(int)

    # Engineered features (paper Section IV)
    df["grade_trend"]   = df["G2"] - df["G1"]
    df["parent_edu"]    = df["Medu"] + df["Fedu"]
    df["support_total"] = (df["schoolsup"] == "yes").astype(int) + \
                          (df["famsup"] == "yes").astype(int)

    return df


def encode_categoricals(df: pd.DataFrame):
    """Label-encode categorical columns. Returns (encoded_df, le_dict)."""
    le_dict = {}
    df_enc = df.copy()
    for col in CATEGORICAL_COLS:
        if col in df_enc.columns:
            le = LabelEncoder()
            df_enc[col] = le.fit_transform(df_enc[col].astype(str))
            le_dict[col] = le
    return df_enc, le_dict


# ── Training ───────────────────────────────────────────────────────────────────

def train(data_path: str, output_path: str):
    print(f"\n{'='*60}")
    print("  EarlyGuard — Training Pipeline")
    print(f"{'='*60}\n")

    # ── Load data ──────────────────────────────────────────────────────────────
    print(f"[1/5] Loading data from: {data_path}")
    df = load_and_prepare(data_path)
    print(f"      {len(df)} students · {df['at_risk'].sum()} at-risk "
          f"({df['at_risk'].mean():.1%})\n")

    # ── Encode ────────────────────────────────────────────────────────────────
    print("[2/5] Encoding categorical features ...")
    df_enc, le_dict = encode_categoricals(df)

    # support_total already numeric after load_and_prepare, but re-encode
    # just in case the raw column is still string-based for famsup/schoolsup.
    # (load_and_prepare already converts them — this is a safety pass.)

    X_s1 = df_enc[STAGE1_FEATURES]
    X_s2 = df_enc[STAGE2_FEATURES]
    y    = df_enc["at_risk"]

    X_s1_tr, X_s1_te, y_tr, y_te = train_test_split(
        X_s1, y, test_size=0.2, random_state=42, stratify=y
    )
    X_s2_tr = df_enc.loc[X_s1_tr.index, STAGE2_FEATURES]
    X_s2_te = df_enc.loc[X_s1_te.index, STAGE2_FEATURES]
    print(f"      Train: {len(X_s1_tr)} · Test: {len(X_s1_te)}\n")

    # ── Stage 1 — Logistic Regression ─────────────────────────────────────────
    print("[3/5] Training Stage 1 — Logistic Regression ...")
    lr = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
        C=1.0,
    )
    lr.fit(X_s1_tr, y_tr)

    p1_te   = lr.predict_proba(X_s1_te)[:, 1]
    s1_pred = (p1_te >= STAGE1_THRESHOLD).astype(int)
    s1_rec  = recall_score(y_te, s1_pred)
    print(f"      Recall @ threshold {STAGE1_THRESHOLD:.2f}: {s1_rec:.3f}\n")

    # ── Stage 2 — RF + XGBoost ────────────────────────────────────────────────
    print("[4/5] Training Stage 2 — RF + XGBoost ensemble ...")

    # Use only Stage-1-flagged samples (simulates production behaviour)
    flagged_tr = X_s1_tr.index[lr.predict_proba(X_s1_tr)[:, 1] >= STAGE1_THRESHOLD]
    X_s2_tr_f  = df_enc.loc[flagged_tr, STAGE2_FEATURES]
    y_tr_f     = y_tr.loc[flagged_tr]

    # If too few flagged samples for Stage 2, fall back to full training set
    if len(X_s2_tr_f) < 30:
        print("      Warning: few flagged samples — training Stage 2 on full set.")
        X_s2_tr_f, y_tr_f = X_s2_tr, y_tr

    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_s2_tr_f, y_tr_f)

    # Scale pos weight for XGBoost (handles imbalance)
    neg = int((y_tr_f == 0).sum())
    pos = int((y_tr_f == 1).sum())
    spw = neg / pos if pos > 0 else 1.0

    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=spw,
        random_state=42,
        eval_metric="logloss",
        verbosity=0,
    )
    xgb.fit(X_s2_tr_f, y_tr_f)

    # ── Evaluate Stage 2 on test set (flagged by Stage 1) ─────────────────────
    flagged_te = X_s1_te.index[p1_te >= STAGE1_THRESHOLD]
    X_s2_te_f  = df_enc.loc[flagged_te, STAGE2_FEATURES]
    y_te_f     = y_te.loc[flagged_te]

    if len(flagged_te) > 0:
        p_rf  = rf.predict_proba(X_s2_te_f)[:, 1]
        p_xgb = xgb.predict_proba(X_s2_te_f)[:, 1]
        p2    = (p_rf + p_xgb) / 2
        s2_pred = (p2 >= 0.50).astype(int)

        f1  = f1_score(y_te_f, s2_pred, zero_division=0)
        pr  = precision_score(y_te_f, s2_pred, zero_division=0)
        rc  = recall_score(y_te_f, s2_pred, zero_division=0)
        auc = roc_auc_score(y_te_f, p2) if len(np.unique(y_te_f)) > 1 else float("nan")

        print(f"\n      Stage 2 Performance (on Stage-1-flagged test students):")
        print(f"      F1={f1:.3f}  Precision={pr:.3f}  Recall={rc:.3f}  AUC={auc:.3f}\n")
        print("      Classification report:")
        print(classification_report(y_te_f, s2_pred, target_names=["Not at risk", "At risk"]))
    else:
        print("      No students flagged in test set — Stage 2 metrics skipped.\n")

    # ── Feature importance (soft-voting ensemble average) ─────────────────────
    rf_imp  = dict(zip(STAGE2_FEATURES, rf.feature_importances_))
    xgb_imp = dict(zip(STAGE2_FEATURES, xgb.feature_importances_))
    feat_importance = {
        f: (rf_imp.get(f, 0) + xgb_imp.get(f, 0)) / 2
        for f in STAGE2_FEATURES
    }
    # Normalise to sum = 1
    total = sum(feat_importance.values())
    if total > 0:
        feat_importance = {k: v / total for k, v in feat_importance.items()}

    # ── Save artefacts ────────────────────────────────────────────────────────
    print(f"[5/5] Saving model artefacts to: {output_path}")
    model_data = {
        "lr_model":           lr,
        "rf_model":           rf,
        "xgb_model":          xgb,
        "le_dict":            le_dict,
        "cat_cols":           CATEGORICAL_COLS,
        "stage1_features":    STAGE1_FEATURES,
        "stage2_features":    STAGE2_FEATURES,
        "stage1_threshold":   STAGE1_THRESHOLD,
        "feature_importance": feat_importance,
    }
    with open(output_path, "wb") as f:
        pickle.dump(model_data, f)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"      Saved ({size_kb:.1f} KB)\n")
    print(f"{'='*60}")
    print("  Training complete.")
    print(f"{'='*60}\n")


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train EarlyGuard two-stage at-risk student detection model."
    )
    parser.add_argument(
        "--data",
        default="data/student-mat.csv",
        help="Path to UCI student-mat.csv (default: student-mat.csv)",
    )
    parser.add_argument(
        "--output",
        default="model_data.pkl",
        help="Output path for model_data.pkl (default: model_data.pkl)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"\n[ERROR] Dataset not found: {args.data}")
        print("  Download from: https://archive.ics.uci.edu/dataset/320/student+performance")
        print("  Then run: python train.py --data student-mat.csv\n")
        raise SystemExit(1)

    train(args.data, args.output)
