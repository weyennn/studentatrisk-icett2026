"""
pages/overview.py
-----------------
Dataset statistics page — UCI Student Performance (Mathematics subset).
"""

import streamlit as st
import pandas as pd
import os

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

# ── Summary metrics ───────────────────────────────────────────────────────
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
      <div class="metric-note">Out of 20 · passing ≥ 10</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Key insights───────────────────────────────────────────────────────
st.markdown("""
<div class="card" style="margin-top:0.5rem;">
  <div class="section-label">Key insights</div>
  <div style="font-size:0.8rem;color:#374151;line-height:1.7;">
    • Approximately one-third of students (≈33%) are classified as at-risk (G3 &lt; 10), indicating a substantial need for early intervention.<br><br>
    • Grade distributions show clustering around the passing threshold (10), suggesting many students are borderline and sensitive to small performance changes.<br><br>
    • Failures and absenteeism exhibit skewed distributions — a small subset of students contributes disproportionately to high-risk signals.<br><br>
    • These patterns justify the use of a two-stage model: early screening captures potential risk, while Stage 2 refines predictions using stronger academic signals.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Key takeaway ────────────────────────────────────────────────────────────
st.markdown("""
<div class="callout">
  <strong>Key takeaway:</strong>
  Many students are not failing yet — they are <em>borderline</em>.
  This makes early detection critical, as small interventions can prevent failure.
</div>
""", unsafe_allow_html=True)

# ── Grade distributions ───────────────────────────────────────────────────
st.markdown('<div class="section-label">Grade distribution</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;font-weight:500;color:#111827;margin-bottom:10px;">First term grade (G1)</div>', unsafe_allow_html=True)
    st.bar_chart(df["G1"].value_counts().sort_index(), height=180, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;font-weight:500;color:#111827;margin-bottom:10px;">Final grade (G3)</div>', unsafe_allow_html=True)
    st.bar_chart(df["G3"].value_counts().sort_index(), height=180, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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

# ── Key feature breakdown ─────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:1rem;">Key feature breakdown</div>', unsafe_allow_html=True)
col_c, col_d, col_e = st.columns(3)

with col_c:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;font-weight:500;color:#111827;margin-bottom:8px;">Failures distribution</div>', unsafe_allow_html=True)
    for k, v in df["failures"].value_counts().sort_index().items():
        pct = v / n_total
        st.markdown(f"""
        <div class="pbar-wrap">
          <div class="pbar-row">
            <span class="pbar-name">{k} failure(s)</span>
            <span class="pbar-val">{v} students</span>
          </div>
          <div class="pbar-bg">
            <div class="pbar-fill" style="width:{int(pct*100)}%;background:#dc2626;"></div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;font-weight:500;color:#111827;margin-bottom:8px;">Weekly study time</div>', unsafe_allow_html=True)
    study_map = {1: "< 2 hrs", 2: "2–5 hrs", 3: "5–10 hrs", 4: "> 10 hrs"}
    for k, v in df["studytime"].value_counts().sort_index().items():
        pct = v / n_total
        st.markdown(f"""
        <div class="pbar-wrap">
          <div class="pbar-row">
            <span class="pbar-name">{study_map.get(k, k)}</span>
            <span class="pbar-val">{v} students</span>
          </div>
          <div class="pbar-bg">
            <div class="pbar-fill" style="width:{int(pct*100)}%;background:#2563eb;"></div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_e:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;font-weight:500;color:#111827;margin-bottom:8px;">Higher education aspiration</div>', unsafe_allow_html=True)
    for k, v in df["higher"].value_counts().items():
        pct   = v / n_total
        color = "#16a34a" if k == "yes" else "#dc2626"
        label = "Aspires to higher ed" if k == "yes" else "Does not aspire"
        st.markdown(f"""
        <div class="pbar-wrap">
          <div class="pbar-row">
            <span class="pbar-name">{label}</span>
            <span class="pbar-val">{v} students</span>
          </div>
          <div class="pbar-bg">
            <div class="pbar-fill" style="width:{int(pct*100)}%;background:{color};"></div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Absence distribution ──────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:1rem;">Absence distribution (top 10 values)</div>', unsafe_allow_html=True)
absence_counts = df["absences"].value_counts().head(10)
absence_max    = absence_counts.max()
st.markdown('<div class="card">', unsafe_allow_html=True)
for k, v in absence_counts.items():
    bar_w = int((v / absence_max) * 100)
    color = "#dc2626" if k >= 10 else "#6b7280"

    st.markdown(f"""
    <div class="pbar-wrap">
      <div class="pbar-row">
        <span class="pbar-name">{k} absence(s){' ⚠' if k >= 10 else ''}</span>
        <span class="pbar-val">{v} students</span>
      </div>
      <div class="pbar-bg">
        <div class="pbar-fill" style="width:{bar_w}%;background:{color};"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
  <div style="font-size:0.72rem;color:#9ca3af;margin-top:0.5rem;">
    ⚠ ≥ 10 absences = high-risk threshold in EarlyGuard intervention logic.
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
