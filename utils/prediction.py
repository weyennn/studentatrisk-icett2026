"""
utils/prediction.py
-------------------
Feature engineering and two-stage inference pipeline.
Intervention logic is rule-based, mapping dominant risk factors to educational
support actions as described in the paper (ICETT 2026, Section III-B & Table III).
"""

import pandas as pd
from config.constants import (
    STAGE2_THRESHOLD,
    RISK_HIGH_THRESHOLD,
    RISK_MEDIUM_THRESHOLD,
    RISK_LABELS,
    ABSENCE_HIGH_THRESHOLD,
    GRADE_DECLINE_CRITICAL,
    GRADE_DECLINE_MODERATE,
    G2_FAIL_THRESHOLD,
)


# ── Feature encoding ──────────────────────────────────────────────────────────

def _encode_val(col: str, val, le_dict: dict):
    """Label-encode a categorical value if an encoder exists for the column."""
    if col in le_dict:
        return le_dict[col].transform([val])[0]
    return val


def build_features(raw: dict, models: dict) -> dict:
    """
    Encode categorical columns and add engineered features.

    Engineered features (paper Section IV):
    - grade_trend   : G2 − G1  (grade progression indicator)
    - parent_edu    : Medu + Fedu  (combined parental education)
    - support_total : schoolsup + famsup  (combined support indicators)
    """
    le       = models["le_dict"]
    cat_cols = models["cat_cols"]

    enc = {}
    for k, v in raw.items():
        enc[k] = _encode_val(k, v, le) if k in cat_cols else v

    enc["grade_trend"]   = raw["G2"] - raw["G1"]
    enc["parent_edu"]    = enc["Medu"] + enc["Fedu"]
    enc["support_total"] = enc["schoolsup"] + enc["famsup"]
    return enc


# ── Two-stage inference ───────────────────────────────────────────────────────

def run_prediction(enc: dict, models: dict) -> dict:
    """
    Execute the two-stage prediction pipeline.

    Stage 1 — Logistic Regression on early-stage features (G1 + demographics +
    behaviour). Low threshold (p1 >= stage1_threshold) prioritises recall so no
    at-risk student is missed.

    Stage 2 — RF + XGBoost soft-voting ensemble on mid-term features (G1, G2,
    grade_trend + all Stage 1 features). Triggered only when Stage 1 flags a
    student. Produces a refined risk probability (p2).

    Returns a result dict consumed by the prediction page.
    """
    lr        = models["lr_model"]
    rf        = models["rf_model"]
    xgb       = models["xgb_model"]
    s1_feats  = models["stage1_features"]
    s2_feats  = models["stage2_features"]
    threshold = models["stage1_threshold"]   # Should be 0.20 per paper
    feat_imp  = models["feature_importance"]

    df_s1 = pd.DataFrame([enc])[s1_feats]
    df_s2 = pd.DataFrame([enc])[s2_feats]

    # Stage 1
    p1      = lr.predict_proba(df_s1)[0, 1]
    flagged = p1 >= threshold

    # Stage 2 (conditional)
    if flagged:
        p_rf  = rf.predict_proba(df_s2)[0, 1]
        p_xgb = xgb.predict_proba(df_s2)[0, 1]
        p2    = (p_rf + p_xgb) / 2          # Soft voting (equal weights)
        final_risk    = p2
        at_risk       = p2 >= STAGE2_THRESHOLD
        stage_reached = 2
    else:
        p2            = None
        final_risk    = p1
        at_risk       = False
        stage_reached = 1

    # Risk level classification
    if final_risk >= RISK_HIGH_THRESHOLD:
        risk_level = "high"
    elif final_risk >= RISK_MEDIUM_THRESHOLD:
        risk_level = "medium"
    else:
        risk_level = "low"

    # Top 5 features by importance (from model, for runtime display)
    top_feats = sorted(feat_imp.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "p1":            p1,
        "p2":            p2,
        "flagged":       flagged,
        "final_risk":    final_risk,
        "at_risk":       at_risk,
        "stage_reached": stage_reached,
        "risk_level":    risk_level,
        "risk_label":    RISK_LABELS[risk_level],
        "grade_trend":   enc["grade_trend"],
        "top_feats":     top_feats,
        "stage1_threshold": threshold,
    }


# ── Intervention recommendations ──────────────────────────────────────────────

def build_interventions(result: dict, raw: dict) -> list[dict]:
    """
    Map dominant risk factors to educational interventions.

    Logic mirrors the paper's intervention mechanism (Section III-B, Table III):
    rule-based mapping from common academic risk patterns (low intermediate
    grades, declining grade trends, frequent absences, prior failures) to
    concrete educational support actions (tutoring, academic advising, attendance
    counseling, remedial programs).

    Each item: {level, title, desc, linked_factor}
    - level         : 'critical' | 'high' | 'moderate'
    - linked_factor : the risk factor (from paper Table III) that triggered this
    """
    G1       = raw["G1"]
    G2       = raw["G2"]
    absences = raw["absences"]
    failures = raw["failures"]
    gt       = result["grade_trend"]

    items = []

    # ── Critical interventions ─────────────────────────────────────────────────
    # Triggered by: G2 (most influential factor, importance 0.324)
    if G2 < G2_FAIL_THRESHOLD:
        items.append({
            "level":         "critical",
            "linked_factor": "Second term grade (G2) — importance 0.324",
            "title":         "Academic tutoring & additional practice",
            "desc": (
                f"G2 = {G2}/20 is below the passing threshold (10). "
                "Arrange immediate one-on-one or small-group tutoring sessions "
                "focused on subject mastery before the final examination period. "
                "G2 is the strongest predictor of final academic outcome in this framework."
            ),
        })

    # Triggered by: grade_trend (importance 0.118) — severe decline
    if gt <= GRADE_DECLINE_CRITICAL:
        items.append({
            "level":         "critical",
            "linked_factor": "Grade trend (G2 − G1) — importance 0.118",
            "title":         "Academic recovery plan",
            "desc": (
                f"Grade dropped {abs(gt)} point(s) from G1 ({G1}) to G2 ({G2}). "
                "Assign an academic advisor to develop a structured recovery plan "
                "with weekly check-ins and targeted mid-course corrections."
            ),
        })

    # ── High interventions ─────────────────────────────────────────────────────
    # Triggered by: absences (importance 0.186)
    if absences >= ABSENCE_HIGH_THRESHOLD:
        items.append({
            "level":         "high",
            "linked_factor": "Number of absences — importance 0.186",
            "title":         "Attendance counseling & monitoring",
            "desc": (
                f"Student has {absences} recorded absences, above the high-risk threshold ({ABSENCE_HIGH_THRESHOLD}). "
                "Schedule a session with the guidance counselor to identify attendance barriers "
                "and establish a formal attendance contract with regular follow-up."
            ),
        })

    # Triggered by: failures (importance 0.142)
    if failures >= 1:
        items.append({
            "level":         "high",
            "linked_factor": "Past course failures — importance 0.142",
            "title":         "Remedial coursework & peer mentoring",
            "desc": (
                f"Student has {failures} prior course failure(s). "
                "Enrol in remedial support programmes and pair with a peer mentor "
                "to address foundational skill gaps before they compound."
            ),
        })

    # ── Moderate interventions ─────────────────────────────────────────────────
    # Triggered by: grade_trend (moderate decline)
    if GRADE_DECLINE_MODERATE > gt > GRADE_DECLINE_CRITICAL:
        items.append({
            "level":         "moderate",
            "linked_factor": "Grade trend (G2 − G1) — importance 0.118",
            "title":         "Academic advising & study skills support",
            "desc": (
                f"Grade declined {abs(gt)} point(s) from G1 ({G1}) to G2 ({G2}). "
                "Provide workshops on time management, note-taking, and exam preparation. "
                "Assign an academic advisor for bi-weekly check-ins."
            ),
        })

    # Triggered by: G1 (importance 0.095) — improvement noted, sustain momentum
    if G2 >= G2_FAIL_THRESHOLD and G1 < G2_FAIL_THRESHOLD:
        items.append({
            "level":         "moderate",
            "linked_factor": "First term grade (G1) — importance 0.095",
            "title":         "Positive reinforcement & progress monitoring",
            "desc": (
                f"Grade improved from G1 = {G1} to G2 = {G2}. "
                "Maintain regular check-ins to sustain this positive trend "
                "and prevent regression before the final assessment."
            ),
        })

    # ── Fallback ───────────────────────────────────────────────────────────────
    if not items:
        items.append({
            "level":         "moderate",
            "linked_factor": "General monitoring",
            "title":         "General academic monitoring",
            "desc": (
                "No single dominant risk indicator detected at this time. "
                "Implement light-touch monitoring: monthly check-ins with the "
                "homeroom teacher and early alert if G3 preliminary scores decline."
            ),
        })

    return items
