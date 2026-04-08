"""
pages/about.py
--------------
Framework overview, methodology, and authors page.

Changes from v1:
- Feature importance values now match paper Table III exactly
  (G2=0.324, absences=0.186, failures=0.142, grade_trend=0.118, G1=0.095)
- Added plain-language explanation of how interventions are selected and
  linked to risk factors (addresses reviewer comment on layman's language)
- Intervention mapping table now shown explicitly per Table III
"""

import streamlit as st
from config.constants import (
    PAPER_FEATURE_IMPORTANCE,
    PAPER_INTERVENTION_MAP,
    AUTHORS,
    DATASET_INFO,
    FEATURE_LABELS,
)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div>
    <div class="page-title">About EarlyGuard</div>
    <div class="page-sub">Intelligent Two-Stage Ensemble Framework for Early Detection of At-Risk Students</div>
  </div>
  <div class="header-badges">
    <span class="hbadge accent">ICETT 2026</span>
    <span class="hbadge">Universitas Gadjah Mada</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Framework overview ────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Framework overview</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    <div class="card">
      <div style="font-size:0.82rem;font-weight:600;color:#111827;margin-bottom:6px;">Stage 1 — Early Screening</div>
      <div style="font-size:0.8rem;color:#4b5563;line-height:1.7;margin-bottom:10px;">
        Uses <strong>Logistic Regression</strong> on first-term data (G1 + demographics + behaviour).
        The classification threshold is deliberately set low (p &ge; 0.20) to maximise recall —
        the priority is to ensure no at-risk student is missed at this early stage, even at the
        cost of some false positives.
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <span class="hbadge">Logistic Regression</span>
        <span class="hbadge">Threshold p &ge; 0.20</span>
        <span class="hbadge success">Maximise Recall</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="card">
      <div style="font-size:0.82rem;font-weight:600;color:#111827;margin-bottom:6px;">Stage 2 — Ensemble Confirmation</div>
      <div style="font-size:0.8rem;color:#4b5563;line-height:1.7;margin-bottom:10px;">
        Uses a <strong>Random Forest + XGBoost soft-voting ensemble</strong> on mid-term data
        (G1, G2, grade trend + all Stage 1 features). Only triggered for students flagged in
        Stage 1. The ensemble balances precision and recall to produce a refined risk score (p₂)
        and identifies dominant risk factors for intervention mapping.
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <span class="hbadge accent">Random Forest</span>
        <span class="hbadge accent">XGBoost</span>
        <span class="hbadge accent">Soft Voting</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Model performance ─────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Stage 2 ensemble performance (test set)</div>', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)
metrics = [
    ("F1-Score",  "0.88",  "Stage 2 ensemble"),
    ("Precision", "0.88",  "Stage 2 ensemble"),
    ("Recall",    "0.88",  "Stage 2 ensemble"),
    ("ROC-AUC",   "0.911", "Stage 2 ensemble"),
]
for col, (label, val, note) in zip([p1, p2, p3, p4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value info">{val}</div>
          <div class="metric-note">{note}</div>
        </div>""", unsafe_allow_html=True)

# ── Key risk factors & intervention mapping ────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Risk factors & intervention mapping (paper Table III)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <strong>How interventions are selected:</strong>&nbsp;
  The Stage 2 ensemble extracts feature importance scores to identify which factors
  most strongly influence a student's risk classification. These dominant factors are
  then matched to concrete educational support actions using a rule-based mapping
  (paper Section III-B). The table below shows this mapping — each risk factor
  directly triggers a specific intervention when its associated threshold is exceeded.
</div>
""", unsafe_allow_html=True)

# Build the mapping table from paper constants
max_imp = PAPER_FEATURE_IMPORTANCE[0][1]

st.markdown("""
<div class="card">
  <div style="display:grid;grid-template-columns:1.8fr 0.6fr 2fr;gap:10px;
              padding:0 0 0.5rem;margin-bottom:0.25rem;">
    <div class="section-label" style="margin:0;">Risk factor</div>
    <div class="section-label" style="margin:0;text-align:center;">Importance</div>
    <div class="section-label" style="margin:0;">Recommended intervention</div>
  </div>
""", unsafe_allow_html=True)

for (feat, imp), (_, intervention) in zip(PAPER_FEATURE_IMPORTANCE, PAPER_INTERVENTION_MAP):

    label = FEATURE_LABELS.get(feat, feat)
    bar_w = int((imp / max_imp) * 100)
    rank_color = "#dc2626" if imp / max_imp > 0.5 else ("#d97706" if imp / max_imp > 0.3 else "#6b7280")

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1.8fr 0.6fr 2fr;gap:10px;align-items:center;
                padding:0.7rem 0;border-bottom:1px solid #f3f4f6;">
      <div>
        <div style="font-size:0.8rem;font-weight:500;color:#111827;">{label}</div>
        <div class="pbar-bg" style="margin-top:5px;">
          <div class="pbar-fill" style="width:{bar_w}%;background:{rank_color};"></div>
        </div>
      </div>
      <div style="font-size:0.78rem;font-weight:600;color:{rank_color};
                  font-family:'DM Mono',monospace;text-align:center;">{imp:.3f}</div>
      <div style="font-size:0.78rem;color:#4b5563;">{intervention}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
  <div style="font-size:0.72rem;color:#9ca3af;margin-top:0.75rem;">
    Source: Paper Table III — Feature importance from Stage 2 RF + XGBoost ensemble.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Plain-language methodology ─────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">For educators — what this framework does in plain language</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
  <div style="font-size:0.82rem;color:#374151;line-height:1.8;">
    <p style="margin:0 0 0.85rem;">
      <strong>The core idea is simple:</strong> instead of waiting until the end of a school year
      to identify struggling students, EarlyGuard raises an early flag after the first assessment
      period — and then confirms that flag using mid-term grades before the final exam.
    </p>
    <p style="margin:0 0 0.85rem;">
      <strong>Why two stages?</strong> Early data is limited, so a single early prediction can
      generate too many false alarms. By adding a confirmation step, the framework reduces
      unnecessary interventions while still acting early enough to make a difference.
    </p>
    <p style="margin:0 0 0.85rem;">
      <strong>Why these interventions?</strong> The model learns which student characteristics
      most reliably predict academic failure — in this dataset, the second-term grade (G2),
      attendance record, prior failures, and grade trend between G1 and G2 are the strongest
      signals. Each recommended intervention directly addresses the factor that raised the alarm:
      poor G2 → tutoring; high absences → attendance counseling; prior failures → remedial support.
    </p>
    <p style="margin:0;">
      <strong>How should the guidance office use this?</strong> EarlyGuard is a decision-support
      tool, not a replacement for educator judgment. Use the risk score and factor list as a
      starting point for a conversation with the student. The four-week protocol on the Prediction
      page shows a recommended workflow from flagging to support plan.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Dataset info ──────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Dataset</div>', unsafe_allow_html=True)

d1, d2, d3, d4 = st.columns(4)
for col, (label, val) in zip(
    [d1, d2, d3, d4],
    [
        ("Dataset",    DATASET_INFO["name"]),
        ("Subject",    DATASET_INFO["subject"]),
        ("Students",   str(DATASET_INFO["students"])),
        ("At-risk %",  DATASET_INFO["class_imbalance"]),
    ]
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div style="font-size:0.88rem;font-weight:600;color:#111827;margin-top:4px;">{val}</div>
        </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="card-tight" style="margin-top:0.75rem;font-size:0.77rem;color:#6b7280;">
  At-risk definition: {DATASET_INFO['at_risk_definition']}&nbsp; · &nbsp;
  Citation: {DATASET_INFO['citation']}&nbsp; · &nbsp;
  <a href="{DATASET_INFO['source']}" target="_blank" style="color:#2563eb;text-decoration:none;">
    UCI Repository ↗
  </a>
</div>
""", unsafe_allow_html=True)

# ── Authors ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Authors</div>', unsafe_allow_html=True)

cols = st.columns(len(AUTHORS))
for col, author in zip(cols, AUTHORS):
    with col:
        role_html = f'<div class="author-role">★ {author["role"]}</div>' if author["role"] else ""
        st.markdown(f"""
        <div class="author-card">
          <div class="author-avatar">{author['initials']}</div>
          <div class="author-name">{author['name']}</div>
          {role_html}
          <div class="author-dept">{author['dept']}<br>{author['univ']}</div>
          <div class="author-email">{author['email']}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="card-tight" style="margin-top:1rem;font-size:0.77rem;color:#6b7280;text-align:center;">
  Supported by the Indonesian Endowment Fund for Education (LPDP),
  Ministry of Education, Culture, Research, and Technology of the Republic of Indonesia.
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  EarlyGuard &nbsp;·&nbsp; ICETT 2026 &nbsp;·&nbsp; Universitas Gadjah Mada<br>
  <span>UCI Student Performance Dataset &nbsp;·&nbsp; Two-stage ensemble framework</span>
</div>
""", unsafe_allow_html=True)
