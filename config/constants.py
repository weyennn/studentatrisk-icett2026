"""
config/constants.py
-------------------
Single source of truth for EarlyGuard thresholds, labels, feature importance,
and intervention rules — derived directly from the paper (ICETT 2026, Table III).
"""

# ── Stage thresholds ───────────────────────────────────────────────────────────
STAGE1_THRESHOLD_DEFAULT = 0.20   # p1 >= this → flagged for Stage 2 (high-recall)
STAGE2_THRESHOLD         = 0.50   # p2 >= this → at-risk classification

# ── Risk level boundaries ──────────────────────────────────────────────────────
RISK_HIGH_THRESHOLD   = 0.65
RISK_MEDIUM_THRESHOLD = 0.40

# ── Feature importance (paper Table III — Stage 2 ensemble) ───────────────────
# Used for display on About page and top-factors bar chart.
PAPER_FEATURE_IMPORTANCE = [
    ("G2",          0.324),
    ("absences",    0.186),
    ("failures",    0.142),
    ("grade_trend", 0.118),
    ("G1",          0.095),
]

# Human-readable labels for features
FEATURE_LABELS = {
    "G2":          "Second term grade (G2)",
    "G1":          "First term grade (G1)",
    "failures":    "Past course failures",
    "grade_trend": "Grade trend (G2 − G1)",
    "absences":    "Number of absences",
    "nursery":     "Attended nursery school",
    "internet":    "Internet access at home",
    "reason":      "School choice reason",
    "sex":         "Gender",
    "famsize":     "Family size",
    "parent_edu":  "Combined parental education",
    "support_total": "Combined school & family support",
}

# ── Intervention mapping (paper Table III) ────────────────────────────────────
# Each entry: (feature_key, recommended_intervention_text)
PAPER_INTERVENTION_MAP = [
    ("G2",          "Academic tutoring and additional practice"),
    ("absences",    "Attendance counseling and monitoring"),
    ("failures",    "Remedial coursework and mentoring"),
    ("grade_trend", "Academic advising and study skills support"),
    ("G1",          "General academic monitoring"),
]

# ── Rule-based intervention logic ────────────────────────────────────────────
# Thresholds that trigger specific intervention cards in the UI
ABSENCE_HIGH_THRESHOLD  = 10    # absences >= this → attendance counseling (HIGH)
GRADE_DECLINE_CRITICAL  = -2    # grade_trend <= this → recovery plan (CRITICAL)
GRADE_DECLINE_MODERATE  = 0     # grade_trend < 0 → study skills support (MODERATE)
G2_FAIL_THRESHOLD       = 10    # G2 < this → tutoring (CRITICAL)

# ── Risk verdict copy ─────────────────────────────────────────────────────────
RISK_VERDICT = {
    "high":   "Significant risk indicators detected. Immediate intervention recommended.",
    "medium": "Some risk indicators present. Monitoring and preventive support advised.",
    "low":    "No significant risk indicators at this time. Routine monitoring sufficient.",
}

RISK_LABELS = {
    "high":   "High risk",
    "medium": "Moderate risk",
    "low":    "Low risk",
}

# ── Authors ───────────────────────────────────────────────────────────────────
AUTHORS = [
    {
        "initials": "YM",
        "name":     "Yayang Matira",
        "role":     "Corresponding author",
        "dept":     "Dept. of Computer Science and Electronics",
        "univ":     "Universitas Gadjah Mada",
        "email":    "yayangmatira@mail.ugm.ac.id",
    },
    {
        "initials": "MI",
        "name":     "Maulana Ihsan Ahmad",
        "role":     "",
        "dept":     "Dept. of Computer Science and Electronics",
        "univ":     "Universitas Gadjah Mada",
        "email":    "maulanaihsanahmad@mail.ugm.ac.id",
    },
    {
        "initials": "GB",
        "name":     "Guntur Budi Herwanto",
        "role":     "",
        "dept":     "Dept. of Computer Science and Electronics",
        "univ":     "Universitas Gadjah Mada",
        "email":    "gunturbudi@mail.ugm.ac.id",
    },
    {
        "initials": "FM",
        "name":     "Fadel Muhamad",
        "role":     "",
        "dept":     "Dept. of Indonesian Language and Literature Education",
        "univ":     "Universitas Negeri Yogyakarta",
        "email":    "fadelmuhamad.2025@student.uny.ac.id",
    },
]

# ── Dataset info ──────────────────────────────────────────────────────────────
DATASET_INFO = {
    "name":     "UCI Student Performance Dataset",
    "subject":  "Mathematics",
    "students": 395,
    "features": 33,
    "source":   "https://archive.ics.uci.edu/dataset/320/student+performance",
    "citation": "Cortez & Silva, 2008",
    "at_risk_definition": "G3 < 10 (below passing threshold in Portuguese grading system)",
    "class_imbalance":    "34.9% at-risk",
}
