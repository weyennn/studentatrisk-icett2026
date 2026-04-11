"""
pages/overview.py
-----------------
Dataset statistics page — UCI Student Performance (Mathematics subset).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# ── Shared chart config ───────────────────────────────────────────────────────
_FONT   = "DM Sans, system-ui, sans-serif"
_MONO   = "DM Mono, monospace"
_BG     = "rgba(0,0,0,0)"   # transparent — sits inside white cards
_GRID   = "#f1f5f9"
_TEXT   = "#374151"
_MUTED  = "#94a3b8"

def _axis(title=""):
    """Reusable axis config."""
    base = dict(gridcolor=_GRID, linecolor=_GRID,
                tickfont=dict(size=11, color=_MUTED),
                title_font=dict(size=11, color=_MUTED))
    if title:
        base["title"] = title
    return base

def _base_layout(**kwargs):
    """Minimal shared layout — all charts inherit this."""
    return dict(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=dict(family=_FONT, color=_TEXT, size=12),
        margin=kwargs.pop("margin", dict(l=8, r=8, t=36, b=8)),
        hoverlabel=dict(
            bgcolor="#1e293b", font_color="#f1f5f9",
            font_family=_FONT, font_size=12,
            bordercolor="#334155",
        ),
        **kwargs,
    )

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div>
    <div class="page-title">Dataset Overview</div>
    <div class="page-sub">UCI Student Performance — Mathematics · Portuguese secondary school</div>
  </div>
  <div class="header-badges">
    <span class="hbadge">395 students</span>
    <span class="hbadge">33 features</span>
    <span class="hbadge">Cortez &amp; Silva, 2008</span>
  </div>
</div>
""", unsafe_allow_html=True)

DATA_PATH = os.path.join("data", "student-mat.csv")

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, sep=";")

df = load_data()
df["at_risk"] = (df["G3"] < 10).astype(int)

n_total  = len(df)
n_risk   = int(df["at_risk"].sum())
n_safe   = n_total - n_risk
pct_risk = n_risk / n_total
avg_g3   = df["G3"].mean()

# ── Summary metrics ───────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">Total students</div>
      <div class="metric-value">{n_total}</div>
      <div class="metric-note">Full dataset</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">At-risk (G3 &lt; 10)</div>
      <div class="metric-value danger">{n_risk}</div>
      <div class="metric-note down">{pct_risk:.1%} of total</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">Not at risk</div>
      <div class="metric-value success">{n_safe}</div>
      <div class="metric-note up">{1-pct_risk:.1%} of total</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">Avg final grade (G3)</div>
      <div class="metric-value">{avg_g3:.1f}</div>
      <div class="metric-note">Out of 20 · passing &ge; 10</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Callout ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="callout">
  <strong>Key takeaway:</strong>
  Many students are not failing yet — they are <em>borderline</em>.
  This makes early detection critical, as small interventions can prevent failure.
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRADE DISTRIBUTIONS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Grade distribution</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

# ── G1 distribution ───────────────────────────────────────────────────────────
with col_a:
    g1_counts = df["G1"].value_counts().sort_index()
    colors_g1 = ["#dc2626" if g < 10 else "#4f46e5" for g in g1_counts.index]

    fig_g1 = go.Figure()
    fig_g1.add_trace(go.Bar(
        x=g1_counts.index.tolist(),
        y=g1_counts.values.tolist(),
        marker_color=colors_g1,
        marker_line_width=0,
        hovertemplate="Grade %{x}: <b>%{y} students</b><extra></extra>",
    ))
    fig_g1.add_vline(
        x=9.5, line_dash="dot", line_color="#d97706", line_width=1.5,
        annotation_text="Pass threshold",
        annotation_position="top right",
        annotation_font=dict(size=10, color="#d97706", family=_FONT),
    )
    fig_g1.update_layout(
        **_base_layout(
            title=dict(text="First term grade (G1)", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
            showlegend=False, bargap=0.18, height=240,
            xaxis={**_axis("Grade"), "tickmode": "linear", "dtick": 2},
            yaxis=_axis("Students"),
        )
    )
    st.markdown('<div class="card" style="padding-bottom:0.5rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig_g1, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div style="display:flex;gap:12px;padding:0 0.5rem 0.5rem;flex-wrap:wrap;">
      <span style="display:flex;align-items:center;gap:5px;font-size:0.72rem;color:#94a3b8;">
        <span style="width:10px;height:10px;border-radius:2px;background:#dc2626;display:inline-block;"></span>Below passing (&lt; 10)
      </span>
      <span style="display:flex;align-items:center;gap:5px;font-size:0.72rem;color:#94a3b8;">
        <span style="width:10px;height:10px;border-radius:2px;background:#4f46e5;display:inline-block;"></span>Passing (&ge; 10)
      </span>
    </div>
    </div>""", unsafe_allow_html=True)

# ── G3 distribution ───────────────────────────────────────────────────────────
with col_b:
    g3_counts = df["G3"].value_counts().sort_index()
    colors_g3 = ["#dc2626" if g < 10 else "#059669" for g in g3_counts.index]

    fig_g3 = go.Figure()
    fig_g3.add_trace(go.Bar(
        x=g3_counts.index.tolist(),
        y=g3_counts.values.tolist(),
        marker_color=colors_g3,
        marker_line_width=0,
        hovertemplate="Grade %{x}: <b>%{y} students</b><extra></extra>",
    ))
    fig_g3.add_vline(
        x=9.5, line_dash="dot", line_color="#d97706", line_width=1.5,
        annotation_text="Pass threshold",
        annotation_position="top right",
        annotation_font=dict(size=10, color="#d97706", family=_FONT),
    )
    fig_g3.update_layout(
        **_base_layout(
            title=dict(text="Final grade (G3)", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
            showlegend=False, bargap=0.18, height=240,
            xaxis={**_axis("Grade"), "tickmode": "linear", "dtick": 2},
            yaxis=_axis("Students"),
        )
    )
    st.markdown('<div class="card" style="padding-bottom:0.5rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig_g3, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div style="display:flex;gap:12px;padding:0 0.5rem 0.5rem;flex-wrap:wrap;">
      <span style="display:flex;align-items:center;gap:5px;font-size:0.72rem;color:#94a3b8;">
        <span style="width:10px;height:10px;border-radius:2px;background:#dc2626;display:inline-block;"></span>At-risk (&lt; 10)
      </span>
      <span style="display:flex;align-items:center;gap:5px;font-size:0.72rem;color:#94a3b8;">
        <span style="width:10px;height:10px;border-radius:2px;background:#059669;display:inline-block;"></span>Passing (&ge; 10)
      </span>
    </div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RISK BREAKDOWN + G1 vs G2 SCATTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem;">Risk profile</div>', unsafe_allow_html=True)
col_pie, col_scatter = st.columns([1, 2])

# ── Donut: at-risk split ──────────────────────────────────────────────────────
with col_pie:
    fig_donut = go.Figure(go.Pie(
        labels=["At-risk", "Not at risk"],
        values=[n_risk, n_safe],
        hole=0.62,
        marker=dict(colors=["#dc2626", "#059669"], line=dict(color="#ffffff", width=2)),
        textinfo="none",
        hovertemplate="%{label}: <b>%{value} students</b> (%{percent})<extra></extra>",
        direction="clockwise",
        sort=False,
    ))
    fig_donut.add_annotation(
        text=f"<b>{pct_risk:.0%}</b><br><span style='font-size:10px'>at-risk</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color="#dc2626", family=_FONT),
        align="center",
    )
    fig_donut.update_layout(
        **_base_layout(
            title=dict(text="At-risk split", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                font=dict(size=11, color=_MUTED),
            ),
            height=260,
            margin=dict(l=8, r=8, t=36, b=32),
        )
    )
    st.markdown('<div class="card" style="padding-bottom:0.25rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Scatter: G1 vs G2 coloured by at_risk ────────────────────────────────────
with col_scatter:
    df_plot = df.copy()
    df_plot["Risk"] = df_plot["at_risk"].map({1: "At-risk", 0: "Not at risk"})
    df_plot["grade_trend"] = df_plot["G2"] - df_plot["G1"]

    fig_scatter = go.Figure()
    for label, color, sym in [
        ("Not at risk", "#4f46e5", "circle"),
        ("At-risk",     "#dc2626", "circle"),
    ]:
        mask = df_plot["Risk"] == label
        fig_scatter.add_trace(go.Scatter(
            x=df_plot.loc[mask, "G1"],
            y=df_plot.loc[mask, "G2"],
            mode="markers",
            name=label,
            marker=dict(
                color=color, size=5, opacity=0.65,
                symbol=sym, line=dict(width=0),
            ),
            hovertemplate=(
                f"<b>{label}</b><br>"
                "G1: %{x}  ·  G2: %{y}<extra></extra>"
            ),
        ))
    # Quadrant lines at grade 10
    fig_scatter.add_hline(y=9.5, line_dash="dot", line_color="#d97706", line_width=1.2)
    fig_scatter.add_vline(x=9.5, line_dash="dot", line_color="#d97706", line_width=1.2)

    fig_scatter.update_layout(
        **_base_layout(
            title=dict(text="G1 vs G2 — coloured by risk label", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5,
                font=dict(size=11, color=_MUTED),
            ),
            height=260,
            margin=dict(l=8, r=8, t=36, b=32),
            xaxis={**_axis("First term grade (G1)"), "tickmode": "linear", "dtick": 2, "range": [-0.5, 20.5]},
            yaxis={**_axis("Second term grade (G2)"), "tickmode": "linear", "dtick": 2, "range": [-0.5, 20.5]},
        )
    )
    st.markdown('<div class="card" style="padding-bottom:0.25rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div style="font-size:0.72rem;color:#94a3b8;padding:0 0.25rem 0.5rem;">
      Dashed lines mark the passing threshold (grade 10). Students in the bottom-left quadrant are highest risk.
    </div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# KEY FEATURE BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem;">Key feature breakdown</div>', unsafe_allow_html=True)
col_c, col_d, col_e = st.columns(3)

# ── Failures ─────────────────────────────────────────────────────────────────
with col_c:
    fail_counts = df["failures"].value_counts().sort_index()
    fig_fail = go.Figure(go.Bar(
        x=[str(k) for k in fail_counts.index],
        y=fail_counts.values.tolist(),
        marker_color=["#dc2626", "#f97316", "#f59e0b", "#fbbf24"],
        marker_line_width=0,
        hovertemplate="Failures: %{x}<br><b>%{y} students</b><extra></extra>",
    ))
    fig_fail.update_layout(
        **_base_layout(
            title=dict(text="Past course failures", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
            showlegend=False, bargap=0.28, height=220,
            xaxis=_axis("No. of failures"), yaxis=_axis("Students"),
        )
    )
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_fail, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Study time ────────────────────────────────────────────────────────────────
with col_d:
    study_map   = {1: "< 2 hrs", 2: "2–5 hrs", 3: "5–10 hrs", 4: "> 10 hrs"}
    study_c     = df["studytime"].value_counts().sort_index()
    study_blues = ["#c7d2fe", "#818cf8", "#4f46e5", "#312e81"]

    fig_study = go.Figure(go.Bar(
        x=[study_map[k] for k in study_c.index],
        y=study_c.values.tolist(),
        marker_color=study_blues,
        marker_line_width=0,
        hovertemplate="%{x}<br><b>%{y} students</b><extra></extra>",
    ))
    fig_study.update_layout(
        **_base_layout(
            title=dict(text="Weekly study time", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
            showlegend=False, bargap=0.28, height=220,
            xaxis=_axis("Hours/week"), yaxis=_axis("Students"),
        )
    )
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_study, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Higher education ──────────────────────────────────────────────────────────
with col_e:
    higher_c = df["higher"].value_counts()
    fig_higher = go.Figure(go.Pie(
        labels=["Aspires", "Does not"],
        values=[higher_c.get("yes", 0), higher_c.get("no", 0)],
        hole=0.55,
        marker=dict(colors=["#059669", "#dc2626"], line=dict(color="#ffffff", width=2)),
        textinfo="none",
        hovertemplate="%{label}: <b>%{value} students</b> (%{percent})<extra></extra>",
        direction="clockwise",
        sort=False,
    ))
    yes_pct = higher_c.get("yes", 0) / n_total
    fig_higher.add_annotation(
        text=f"<b>{yes_pct:.0%}</b><br><span style='font-size:10px'>aspire</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="#059669", family=_FONT),
        align="center",
    )
    fig_higher.update_layout(
        **_base_layout(
            title=dict(text="Higher education aspiration", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5,
                font=dict(size=11, color=_MUTED),
            ),
            height=220,
            margin=dict(l=8, r=8, t=36, b=24),
        )
    )
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_higher, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ABSENCE DISTRIBUTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem;">Absence distribution (top 15 values)</div>', unsafe_allow_html=True)

absence_counts = df["absences"].value_counts().nlargest(15).sort_index()
colors_abs = ["#dc2626" if k >= 10 else "#4f46e5" for k in absence_counts.index]

fig_abs = go.Figure(go.Bar(
    x=absence_counts.index.tolist(),
    y=absence_counts.values.tolist(),
    marker_color=colors_abs,
    marker_line_width=0,
    hovertemplate="Absences: %{x}<br><b>%{y} students</b><extra></extra>",
))
fig_abs.add_vline(
    x=9.5, line_dash="dot", line_color="#d97706", line_width=1.5,
    annotation_text="High-risk threshold (>= 10)",
    annotation_position="top right",
    annotation_font=dict(size=10, color="#d97706", family=_FONT),
)
fig_abs.update_layout(
    **_base_layout(
        title=dict(text="Number of absences per student", font=dict(size=13, color=_TEXT, family=_FONT), x=0),
        showlegend=False, bargap=0.22, height=240,
        xaxis={**_axis("Absences"), "tickmode": "linear", "dtick": 1},
        yaxis=_axis("Students"),
    )
)

st.markdown('<div class="card" style="padding-bottom:0.5rem;">', unsafe_allow_html=True)
st.plotly_chart(fig_abs, use_container_width=True, config={"displayModeBar": False})
st.markdown("""
<div style="display:flex;gap:16px;padding:0 0.25rem 0.5rem;flex-wrap:wrap;">
  <span style="display:flex;align-items:center;gap:5px;font-size:0.72rem;color:#94a3b8;">
    <span style="width:10px;height:10px;border-radius:2px;background:#4f46e5;display:inline-block;"></span>Normal (&lt; 10 absences)
  </span>
  <span style="display:flex;align-items:center;gap:5px;font-size:0.72rem;color:#94a3b8;">
    <span style="width:10px;height:10px;border-radius:2px;background:#dc2626;display:inline-block;"></span>High-risk (&ge; 10 absences) — triggers attendance counseling
  </span>
</div>
</div>""", unsafe_allow_html=True)

# ── Why this matters ──────────────────────────────────────────────────────────
st.markdown("""
<div class="card" style="margin-top:1rem;">
  <div class="section-label">Why this matters for EarlyGuard</div>
  <div style="font-size:0.8rem;color:#374151;line-height:1.7;">
    The dataset reveals that academic performance (G1, G2) dominates predictive power,
    while behavioural factors (absences, study time) provide supporting signals.
    <br><br>
    This justifies EarlyGuard's architecture:
    <ul style="margin-top:0.5rem;">
      <li>Stage 1 uses broad features for high-recall screening</li>
      <li>Stage 2 focuses on academic trends for precise confirmation</li>
    </ul>
    By combining both, the system balances early detection with prediction reliability.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  EarlyGuard &nbsp;·&nbsp; ICETT 2026 &nbsp;·&nbsp; Universitas Gadjah Mada<br>
  <span>UCI Student Performance Dataset &nbsp;·&nbsp; Two-stage ensemble framework</span>
</div>
""", unsafe_allow_html=True)
