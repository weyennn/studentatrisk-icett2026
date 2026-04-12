"""
pages/about.py
--------------
Framework overview, methodology, and authors page.
"""

import os
import streamlit as st
import plotly.graph_objects as go
from config.constants import (
    PAPER_FEATURE_IMPORTANCE,
    PAPER_INTERVENTION_MAP,
    AUTHORS,
    DATASET_INFO,
    FEATURE_LABELS,
)

_ASSETS     = os.path.join(os.path.dirname(__file__), "..", "assets")
_LOGO_UGM   = os.path.join(_ASSETS, "Logo-Tengah-Stack-Up-1.jpg")
_LOGO_ICETT = os.path.join(_ASSETS, "logo icett.png")

_FONT = "DM Sans, system-ui, sans-serif"
_BG   = "rgba(0,0,0,0)"
_GRID = "#f1f5f9"
_TEXT = "#374151"
_MUTED = "#94a3b8"

# ── Institutional logos ───────────────────────────────────────────────────────
_lpad, _lugm, _gap, _licett, _rpad = st.columns([2, 1.5, 0.5, 1.5, 2])
with _lugm:
    if os.path.exists(_LOGO_UGM):
        st.image(_LOGO_UGM, use_container_width=True)
with _licett:
    if os.path.exists(_LOGO_ICETT):
        st.image(_LOGO_ICETT, use_container_width=True)

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

# ═══════════════════════════════════════════════════════════════════════════════
# PIPELINE FLOW VISUAL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Detection pipeline</div>', unsafe_allow_html=True)

_p1, _a1, _p2, _a2, _p3, _a3, _p4, _a4, _p5 = st.columns([3, 0.6, 3.5, 0.6, 2.5, 0.6, 3.5, 0.6, 3])

with _p1:
    st.markdown("""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;
                padding:1.25rem 1rem;text-align:center;height:100%;">
      <div style="font-size:0.65rem;font-weight:800;text-transform:uppercase;
                  letter-spacing:0.1em;color:#94a3b8;margin-bottom:6px;">Input</div>
      <div style="font-size:0.9rem;font-weight:700;color:#0f172a;margin-bottom:4px;">Student Data</div>
      <div style="font-size:0.72rem;color:#64748b;line-height:1.6;">33 features<br>Demographics<br>Academic records</div>
    </div>""", unsafe_allow_html=True)

with _a1:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;height:100%;
                font-size:1.6rem;color:#c7d2fe;padding-top:0.5rem;">&#10142;</div>
    """, unsafe_allow_html=True)

with _p2:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#eff6ff,#eef2ff);border:1px solid #c7d2fe;
                border-top:3px solid #4f46e5;border-radius:14px;padding:1.25rem 1rem;text-align:center;height:100%;">
      <div style="font-size:0.65rem;font-weight:800;text-transform:uppercase;
                  letter-spacing:0.12em;color:#4f46e5;margin-bottom:6px;">Stage 1</div>
      <div style="font-size:0.9rem;font-weight:700;color:#0f172a;margin-bottom:4px;">Early Screening</div>
      <div style="font-size:0.75rem;color:#6366f1;font-weight:600;margin-bottom:8px;">Logistic Regression</div>
      <div style="font-size:0.71rem;color:#64748b;line-height:1.65;">G1 + demographics<br>+ behaviour<br>
        <span style="background:#e0e7ff;color:#4338ca;padding:1px 6px;border-radius:4px;
                     font-weight:600;font-size:0.68rem;">threshold p &ge; 0.20</span>
      </div>
    </div>""", unsafe_allow_html=True)

with _a2:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;height:100%;
                font-size:1.6rem;color:#c7d2fe;padding-top:0.5rem;">&#10142;</div>
    """, unsafe_allow_html=True)

with _p3:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1px solid #fde68a;
                border-top:3px solid #d97706;border-radius:14px;padding:1.25rem 0.75rem;text-align:center;height:100%;">
      <div style="font-size:0.65rem;font-weight:800;text-transform:uppercase;
                  letter-spacing:0.1em;color:#d97706;margin-bottom:4px;">Gate</div>
      <div style="font-size:0.88rem;font-weight:700;color:#0f172a;">Flagged?</div>
      <div style="font-size:0.7rem;color:#92400e;margin-top:6px;line-height:1.6;">
        p &ge; 0.20<br>→ proceed to<br>Stage 2
      </div>
    </div>""", unsafe_allow_html=True)

with _a3:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;height:100%;
                font-size:1.6rem;color:#c7d2fe;padding-top:0.5rem;">&#10142;</div>
    """, unsafe_allow_html=True)

with _p4:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);border:1px solid #c4b5fd;
                border-top:3px solid #7c3aed;border-radius:14px;padding:1.25rem 1rem;text-align:center;height:100%;">
      <div style="font-size:0.65rem;font-weight:800;text-transform:uppercase;
                  letter-spacing:0.12em;color:#7c3aed;margin-bottom:6px;">Stage 2</div>
      <div style="font-size:0.9rem;font-weight:700;color:#0f172a;margin-bottom:4px;">Confirmation</div>
      <div style="font-size:0.75rem;color:#7c3aed;font-weight:600;margin-bottom:8px;">RF + XGBoost Ensemble</div>
      <div style="font-size:0.71rem;color:#64748b;line-height:1.65;">G1 + G2 + grade trend<br>+ all Stage 1 features<br>
        <span style="background:#ede9fe;color:#6d28d9;padding:1px 6px;border-radius:4px;
                     font-weight:600;font-size:0.68rem;">soft voting</span>
      </div>
    </div>""", unsafe_allow_html=True)

with _a4:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;height:100%;
                font-size:1.6rem;color:#c7d2fe;padding-top:0.5rem;">&#10142;</div>
    """, unsafe_allow_html=True)

with _p5:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border:1px solid #a7f3d0;
                border-top:3px solid #059669;border-radius:14px;padding:1.25rem 1rem;text-align:center;height:100%;">
      <div style="font-size:0.65rem;font-weight:800;text-transform:uppercase;
                  letter-spacing:0.1em;color:#059669;margin-bottom:6px;">Output</div>
      <div style="font-size:0.9rem;font-weight:700;color:#0f172a;margin-bottom:4px;">Risk Score</div>
      <div style="font-size:0.72rem;color:#64748b;line-height:1.6;">High / Medium / Low<br>+ Intervention<br>recommendations</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE CARDS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div class="card" style="border-top:3px solid #4f46e5;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#4f46e5,#818cf8);
                    display:flex;align-items:center;justify-content:center;
                    font-size:0.75rem;font-weight:800;color:#fff;flex-shrink:0;">1</div>
        <div style="font-size:0.88rem;font-weight:700;color:#0f172a;">Early Screening</div>
      </div>
      <div style="font-size:0.8rem;color:#4b5563;line-height:1.75;margin-bottom:12px;">
        Uses <strong>Logistic Regression</strong> on first-term data (G1 + demographics + behaviour).
        The classification threshold is deliberately set low (p &ge; 0.20) to maximise recall —
        the priority is to ensure no at-risk student is missed at this early stage, even at the
        cost of some false positives.
      </div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;">
        <span class="hbadge">Logistic Regression</span>
        <span class="hbadge">Threshold p &ge; 0.20</span>
        <span class="hbadge success">Maximise Recall</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="card" style="border-top:3px solid #7c3aed;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#7c3aed,#a78bfa);
                    display:flex;align-items:center;justify-content:center;
                    font-size:0.75rem;font-weight:800;color:#fff;flex-shrink:0;">2</div>
        <div style="font-size:0.88rem;font-weight:700;color:#0f172a;">Ensemble Confirmation</div>
      </div>
      <div style="font-size:0.8rem;color:#4b5563;line-height:1.75;margin-bottom:12px;">
        Uses a <strong>Random Forest + XGBoost soft-voting ensemble</strong> on mid-term data
        (G1, G2, grade trend + all Stage 1 features). Only triggered for students flagged in
        Stage 1. Balances precision and recall to produce a refined risk score (p&#8322;)
        and identifies dominant risk factors for intervention mapping.
      </div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;">
        <span class="hbadge accent">Random Forest</span>
        <span class="hbadge accent">XGBoost</span>
        <span class="hbadge accent">Soft Voting</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Stage 2 ensemble performance (full test set, n=79)</div>', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)
metrics = [
    ("F1-Score",  "0.8846", "Stage 2 ensemble", 0.8846),
    ("Precision", "0.8846", "Stage 2 ensemble", 0.8846),
    ("Recall",    "0.8846", "Stage 2 ensemble", 0.8846),
    ("ROC-AUC",   "0.9782", "Stage 2 ensemble", 0.9782),
]
for col, (label, val, note, _pct) in zip([p1, p2, p3, p4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value info">{val}</div>
          <div class="metric-note">{note}</div>
        </div>""", unsafe_allow_html=True)

# ── Radar chart ───────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
categories = ["F1-Score", "Precision", "Recall", "ROC-AUC", "F1-Score"]
values     = [0.8846, 0.8846, 0.8846, 0.9782, 0.8846]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=values, theta=categories,
    fill="toself",
    fillcolor="rgba(99,102,241,0.15)",
    line=dict(color="#6366f1", width=2),
    marker=dict(size=6, color="#6366f1"),
    hovertemplate="%{theta}: <b>%{r:.3f}</b><extra></extra>",
    name="Stage 2 Ensemble",
))
fig_radar.update_layout(
    paper_bgcolor=_BG, plot_bgcolor=_BG,
    font=dict(family=_FONT, color=_TEXT, size=11),
    margin=dict(l=40, r=40, t=20, b=20),
    height=260,
    showlegend=False,
    polar=dict(
        bgcolor=_BG,
        radialaxis=dict(
            range=[0.8, 1.0], tickvals=[0.85, 0.90, 0.95, 1.0],
            tickfont=dict(size=10, color=_MUTED), gridcolor=_GRID,
            linecolor=_GRID,
        ),
        angularaxis=dict(
            tickfont=dict(size=11, color=_TEXT), gridcolor=_GRID, linecolor=_GRID,
        ),
    ),
    hoverlabel=dict(bgcolor="#1e293b", font_color="#f1f5f9", font_family=_FONT, font_size=12),
)

col_radar, col_note = st.columns([1, 1])
with col_radar:
    st.markdown('<div class="card" style="padding-bottom:0.5rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_note:
    st.markdown("""
    <div class="card" style="height:100%;">
      <div class="section-label">Why these metrics matter</div>
      <div style="display:flex;flex-direction:column;gap:10px;margin-top:0.25rem;">
        <div style="padding:0.65rem 0.875rem;background:#f8fafc;border-radius:8px;border-left:3px solid #4f46e5;">
          <div style="font-size:0.78rem;font-weight:700;color:#0f172a;margin-bottom:2px;">F1-Score 0.8846</div>
          <div style="font-size:0.73rem;color:#64748b;line-height:1.55;">Harmonic mean of precision and recall. Confirms the ensemble performs well on both dimensions.</div>
        </div>
        <div style="padding:0.65rem 0.875rem;background:#f8fafc;border-radius:8px;border-left:3px solid #7c3aed;">
          <div style="font-size:0.78rem;font-weight:700;color:#0f172a;margin-bottom:2px;">ROC-AUC 0.9782</div>
          <div style="font-size:0.73rem;color:#64748b;line-height:1.55;">Probability that the model ranks a random at-risk student above a random safe one. 0.9782 indicates strong discrimination.</div>
        </div>
        <div style="padding:0.65rem 0.875rem;background:#f8fafc;border-radius:8px;border-left:3px solid #059669;">
          <div style="font-size:0.78rem;font-weight:700;color:#0f172a;margin-bottom:2px;">Recall 0.8846</div>
          <div style="font-size:0.73rem;color:#64748b;line-height:1.55;">Of all truly at-risk students, 88% are correctly identified. Critical metric for an early-warning system.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# BASELINE COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Baseline comparison (full test set, n=79)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <strong>Evaluation setup:</strong>&nbsp;
  All models are trained on the same 80/20 stratified split (train=316, test=79) using Stage 2 features.
  EarlyGuard is evaluated as a complete two-stage system — Stage 1 flags students, Stage 2 confirms risk.
  Non-flagged students are assigned a risk probability of 0.
</div>
""", unsafe_allow_html=True)

_baseline_data = {
    "Model":     ["Logistic Regression", "Decision Tree", "Random Forest", "XGBoost", "SVM", "EarlyGuard (Ours)"],
    "F1":        [0.8148, 0.8364, 0.8679, 0.8846, 0.8475, 0.8846],
    "Precision": [0.7857, 0.7931, 0.8519, 0.8846, 0.7576, 0.8846],
    "Recall":    [0.8462, 0.8846, 0.8846, 0.8846, 0.9615, 0.8846],
    "AUC":       [0.9681, 0.8857, 0.9681, 0.9623, 0.9688, 0.9782],
    "Accuracy":  [0.8734, 0.8861, 0.9114, 0.9241, 0.8861, 0.9241],
}

import pandas as pd

_models  = _baseline_data["Model"]
_is_ours = [m == "EarlyGuard (Ours)" for m in _models]

_col_tbl, _col_chart = st.columns([1, 1])

with _col_tbl:
    _df = pd.DataFrame({
        "Model":     _baseline_data["Model"],
        "F1":        _baseline_data["F1"],
        "Precision": _baseline_data["Precision"],
        "Recall":    _baseline_data["Recall"],
        "ROC-AUC":   _baseline_data["AUC"],
        "Accuracy":  _baseline_data["Accuracy"],
    }).set_index("Model")

    def _highlight_ours(row):
        if row.name == "EarlyGuard (Ours)":
            return ["background-color:#eef2ff;color:#4338ca;font-weight:700"] * len(row)
        return [""] * len(row)

    def _highlight_best(col):
        is_best = col == col.max()
        return ["font-weight:700;color:#059669" if v else "" for v in is_best]

    _styled = (
        _df.style
        .apply(_highlight_ours, axis=1)
        .apply(_highlight_best, axis=0)
        .format("{:.4f}")
    )
    st.dataframe(_styled, use_container_width=True)

with _col_chart:
    fig_base = go.Figure()
    for metric, color in [("AUC", "#4f46e5"), ("F1", "#7c3aed"), ("Accuracy", "#0284c7")]:
        fig_base.add_trace(go.Bar(
            name=metric,
            x=_models,
            y=_baseline_data[metric],
            marker_color=[color if not o else "#f59e0b" for o in _is_ours],
            marker_line_width=0,
            hovertemplate="%{x}<br>" + metric + ": <b>%{y:.4f}</b><extra></extra>",
        ))
        break  # show AUC only for clarity

    fig_base.update_layout(
        paper_bgcolor=_BG, plot_bgcolor=_BG,
        font=dict(family=_FONT, color=_TEXT, size=11),
        margin=dict(l=8, r=8, t=16, b=80),
        height=280,
        showlegend=False,
        bargap=0.3,
        yaxis=dict(range=[0.85, 1.0], gridcolor=_GRID, linecolor=_GRID,
                   title="ROC-AUC", title_font=dict(size=10, color=_MUTED),
                   tickfont=dict(size=10, color=_MUTED)),
        xaxis=dict(gridcolor=_GRID, linecolor=_GRID,
                   tickfont=dict(size=10, color=_TEXT), tickangle=-20),
        hoverlabel=dict(bgcolor="#1e293b", font_color="#f1f5f9", font_family=_FONT, font_size=12),
    )
    st.markdown('<div class="card" style="padding-bottom:0.25rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig_base, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div style="font-size:0.72rem;color:#94a3b8;padding:0 0.25rem 0.5rem;">
      EarlyGuard (orange) achieves the highest ROC-AUC across all baselines.
    </div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE IMPORTANCE CHART + INTERVENTION MAPPING
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Risk factors &amp; intervention mapping (paper Table III)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <strong>How interventions are selected:</strong>&nbsp;
  The Stage 2 ensemble extracts feature importance scores to identify which factors most strongly
  influence a student's risk classification. These dominant factors are then matched to concrete
  educational support actions using a rule-based mapping (paper Section III-B).
</div>
""", unsafe_allow_html=True)

max_imp    = PAPER_FEATURE_IMPORTANCE[0][1]
feat_names = [FEATURE_LABELS.get(f, f) for f, _ in PAPER_FEATURE_IMPORTANCE]
feat_vals  = [imp for _, imp in PAPER_FEATURE_IMPORTANCE]
feat_colors = ["#4f46e5", "#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe"]

fig_imp = go.Figure()
fig_imp.add_trace(go.Bar(
    x=feat_vals[::-1],
    y=feat_names[::-1],
    orientation="h",
    marker=dict(color=feat_colors[::-1], line=dict(width=0)),
    text=[f"{v:.3f}" for v in feat_vals[::-1]],
    textposition="inside",
    textfont=dict(color="#ffffff", size=11, family=_FONT),
    hovertemplate="%{y}<br>Importance: <b>%{x:.3f}</b><extra></extra>",
))
fig_imp.update_layout(
    paper_bgcolor=_BG, plot_bgcolor=_BG,
    font=dict(family=_FONT, color=_TEXT, size=11),
    margin=dict(l=8, r=8, t=16, b=8),
    height=210,
    showlegend=False,
    bargap=0.28,
    xaxis=dict(
        title="Importance score", range=[0, 0.38],
        gridcolor=_GRID, linecolor=_GRID,
        tickfont=dict(size=10, color=_MUTED), title_font=dict(size=10, color=_MUTED),
    ),
    yaxis=dict(
        gridcolor=_GRID, linecolor=_GRID,
        tickfont=dict(size=11, color=_TEXT),
    ),
    hoverlabel=dict(bgcolor="#1e293b", font_color="#f1f5f9", font_family=_FONT, font_size=12),
)

col_chart, col_map = st.columns([1, 1])
with col_chart:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_imp, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div style="font-size:0.72rem;color:#94a3b8;padding:0 0.25rem 0.5rem;">
      Source: Paper Table III — Stage 2 RF + XGBoost ensemble.
    </div></div>""", unsafe_allow_html=True)

with col_map:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label" style="margin-bottom:0.6rem;">Intervention trigger rules</div>', unsafe_allow_html=True)
    rank_colors = ["#dc2626", "#d97706", "#d97706", "#0284c7", "#0284c7"]
    rank_bgs    = ["#fef2f2", "#fffbeb", "#fffbeb", "#f0f9ff", "#f0f9ff"]
    rank_borders= ["#fca5a5", "#fde68a", "#fde68a", "#bae6fd", "#bae6fd"]
    for i, ((feat, imp), (_, intervention)) in enumerate(
        zip(PAPER_FEATURE_IMPORTANCE, PAPER_INTERVENTION_MAP)
    ):
        label = FEATURE_LABELS.get(feat, feat)
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:10px;padding:0.55rem 0.75rem;
                    background:{rank_bgs[i]};border:1px solid {rank_borders[i]};
                    border-left:3px solid {rank_colors[i]};border-radius:8px;margin-bottom:6px;">
          <div style="flex-shrink:0;width:36px;text-align:center;">
            <div style="font-size:0.65rem;font-weight:800;color:{rank_colors[i]};
                        text-transform:uppercase;letter-spacing:0.05em;">#{i+1}</div>
            <div style="font-size:0.68rem;font-weight:700;color:{rank_colors[i]};
                        font-family:'DM Mono',monospace;">{imp:.3f}</div>
          </div>
          <div>
            <div style="font-size:0.77rem;font-weight:600;color:#0f172a;">{label}</div>
            <div style="font-size:0.71rem;color:#64748b;margin-top:1px;line-height:1.45;">{intervention}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOR EDUCATORS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">For educators — plain language explanation</div>', unsafe_allow_html=True)

qa_items = [
    ("#4f46e5", "#eef2ff", "#c7d2fe",
     "What does EarlyGuard actually do?",
     "Instead of waiting until the end of a school year to identify struggling students, "
     "EarlyGuard raises an early flag after the first assessment period — and then confirms "
     "that flag using mid-term grades before the final exam."),
    ("#7c3aed", "#f5f3ff", "#c4b5fd",
     "Why two stages instead of one?",
     "Early data is limited, so a single early prediction can generate too many false alarms. "
     "By adding a confirmation step, the framework reduces unnecessary interventions while still "
     "acting early enough to make a meaningful difference."),
    ("#0284c7", "#f0f9ff", "#bae6fd",
     "Why these specific interventions?",
     "The model learns which student characteristics most reliably predict academic failure. "
     "In this dataset, G2, attendance, prior failures, and grade trend are the strongest signals. "
     "Each recommended intervention directly addresses the factor that raised the alarm: "
     "poor G2 → tutoring; high absences → attendance counseling; prior failures → remedial support."),
    ("#059669", "#f0fdf4", "#a7f3d0",
     "How should the guidance office use this?",
     "EarlyGuard is a decision-support tool, not a replacement for educator judgment. "
     "Use the risk score and factor list as a starting point for a conversation with the student. "
     "The four-week protocol on the Prediction page shows a recommended workflow from flagging to support plan."),
]

col_q1, col_q2 = st.columns(2)
for i, (border, bg, bord_col, question, answer) in enumerate(qa_items):
    col = col_q1 if i % 2 == 0 else col_q2
    with col:
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {bord_col};border-left:4px solid {border};
                    border-radius:0 12px 12px 0;padding:1rem 1.125rem;margin-bottom:0.75rem;">
          <div style="font-size:0.82rem;font-weight:700;color:#0f172a;margin-bottom:6px;">{question}</div>
          <div style="font-size:0.78rem;color:#475569;line-height:1.7;">{answer}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATASET INFO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Dataset</div>', unsafe_allow_html=True)

d1, d2, d3, d4 = st.columns(4)
for col, (label, val) in zip(
    [d1, d2, d3, d4],
    [
        ("Dataset",   DATASET_INFO["name"]),
        ("Subject",   DATASET_INFO["subject"]),
        ("Students",  str(DATASET_INFO["students"])),
        ("At-risk %", DATASET_INFO["class_imbalance"]),
    ]
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div style="font-size:0.88rem;font-weight:700;color:#0f172a;margin-top:6px;line-height:1.3;">{val}</div>
        </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="card-tight" style="margin-top:0.75rem;font-size:0.77rem;color:#64748b;">
  <strong style="color:#374151;">At-risk definition:</strong> {DATASET_INFO['at_risk_definition']}
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <strong style="color:#374151;">Citation:</strong> {DATASET_INFO['citation']}
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="{DATASET_INFO['source']}" target="_blank"
     style="color:#4f46e5;text-decoration:none;font-weight:500;">UCI Repository ↗</a>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINISI OPERASIONAL VARIABEL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Definisi Operasional Variabel</div>', unsafe_allow_html=True)

_VAR_DEFS = [
    # (variabel, tipe, deskripsi, skala/nilai)
    ("G1",           "Numerik",   "Nilai ujian semester pertama",                          "0 – 20"),
    ("G2",           "Numerik",   "Nilai ujian semester kedua",                            "0 – 20"),
    ("G3",           "Numerik",   "Nilai akhir semester (variabel target)",                "0 – 20; < 10 = at-risk"),
    ("grade_trend",  "Turunan",   "Selisih nilai G2 − G1 (tren akademik antar semester)",  "Negatif = menurun"),
    ("failures",     "Numerik",   "Jumlah kegagalan mata pelajaran sebelumnya",            "0 – 4"),
    ("absences",     "Numerik",   "Jumlah hari tidak hadir dalam setahun",                 "0 – 93"),
    ("sex",          "Kategorikal","Jenis kelamin siswa",                                  "M / F"),
    ("famsize",      "Kategorikal","Ukuran keluarga",                                      "LE3 (≤3) / GT3 (>3)"),
    ("internet",     "Biner",     "Akses internet di rumah",                               "yes / no"),
    ("nursery",      "Biner",     "Pernah mengikuti pendidikan pra-sekolah (TK)",          "yes / no"),
    ("reason",       "Kategorikal","Alasan memilih sekolah",                               "home / reputation / course / other"),
    ("parent_edu",   "Numerik",   "Gabungan tingkat pendidikan ayah dan ibu",              "Skor komposit 0 – 8"),
    ("support_total","Numerik",   "Gabungan dukungan sekolah dan keluarga",                "Skor komposit 0 – 4"),
]

_hdr = ["Variabel", "Tipe Data", "Deskripsi", "Skala / Nilai"]
_hdr_html = "".join(
    f'<th style="padding:8px 12px;text-align:left;font-size:0.72rem;font-weight:700;'
    f'color:#64748b;text-transform:uppercase;letter-spacing:0.06em;'
    f'border-bottom:2px solid #e2e8f0;">{h}</th>'
    for h in _hdr
)

_rows_html = ""
for i, (var, tipe, desc, skala) in enumerate(_VAR_DEFS):
    _bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
    _type_colors = {
        "Numerik":     ("#eff6ff", "#3b82f6"),
        "Turunan":     ("#fdf4ff", "#a855f7"),
        "Kategorikal": ("#fff7ed", "#f97316"),
        "Biner":       ("#f0fdf4", "#22c55e"),
    }
    _tc_bg, _tc_fg = _type_colors.get(tipe, ("#f1f5f9", "#64748b"))
    _rows_html += f"""
    <tr style="background:{_bg};">
      <td style="padding:8px 12px;font-size:0.78rem;font-weight:700;color:#0f172a;
                 border-bottom:1px solid #f1f5f9;font-family:monospace;">{var}</td>
      <td style="padding:8px 12px;border-bottom:1px solid #f1f5f9;">
        <span style="background:{_tc_bg};color:{_tc_fg};font-size:0.68rem;font-weight:700;
                     padding:2px 8px;border-radius:20px;">{tipe}</span>
      </td>
      <td style="padding:8px 12px;font-size:0.78rem;color:#374151;
                 border-bottom:1px solid #f1f5f9;">{desc}</td>
      <td style="padding:8px 12px;font-size:0.76rem;color:#64748b;
                 border-bottom:1px solid #f1f5f9;">{skala}</td>
    </tr>"""

st.markdown(f"""
<div class="card" style="padding:0;overflow:hidden;">
  <table style="width:100%;border-collapse:collapse;">
    <thead><tr style="background:#f8fafc;">{_hdr_html}</tr></thead>
    <tbody>{_rows_html}</tbody>
  </table>
</div>
<div style="font-size:0.72rem;color:#94a3b8;margin-top:6px;">
  Sumber: UCI Student Performance Dataset (Cortez &amp; Silva, 2008).
  G3 digunakan sebagai label; G1 dan G2 digunakan sebagai prediktor pada masing-masing stage.
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# AUTHORS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Authors</div>', unsafe_allow_html=True)

_AVATAR_COLORS = [
    ("linear-gradient(135deg,#4f46e5,#818cf8)", "#fff"),
    ("linear-gradient(135deg,#7c3aed,#a78bfa)", "#fff"),
    ("linear-gradient(135deg,#0284c7,#38bdf8)", "#fff"),
    ("linear-gradient(135deg,#059669,#34d399)", "#fff"),
]

cols = st.columns(len(AUTHORS))
for i, (col, author) in enumerate(zip(cols, AUTHORS)):
    bg, fg = _AVATAR_COLORS[i % len(_AVATAR_COLORS)]
    role_html = (
        f'<div style="font-size:0.68rem;font-weight:700;color:#6366f1;margin-top:3px;'
        f'letter-spacing:0.03em;">Corresponding Author</div>'
        if author["role"] else ""
    )
    with col:
        st.markdown(f"""
        <div class="author-card">
          <div style="width:52px;height:52px;border-radius:50%;background:{bg};
                      display:flex;align-items:center;justify-content:center;
                      margin:0 auto 12px;font-size:0.9rem;font-weight:800;color:{fg};
                      box-shadow:0 4px 12px rgba(99,102,241,0.25);">
            {author['initials']}
          </div>
          <div class="author-name">{author['name']}</div>
          {role_html}
          <div class="author-dept" style="margin-top:5px;">{author['dept']}<br>{author['univ']}</div>
          <div class="author-email">{author['email']}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="card-tight" style="margin-top:1rem;font-size:0.77rem;color:#64748b;text-align:center;">
  Supported by the <strong style="color:#374151;">Indonesian Endowment Fund for Education (LPDP)</strong>,
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
