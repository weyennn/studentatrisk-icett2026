"""
pages/predict.py
----------------
Main prediction dashboard. Two-stage at-risk student detection.

Reviewer comment addressed:
- Interventions are now explicitly linked to dominant risk factors (paper Table III)
- Plain-language descriptions explain WHY each intervention is recommended
- Guidance office protocol section shows HOW the framework is operationalized
"""

import streamlit as st
from utils.model import load_models
from utils.prediction import build_features, run_prediction, build_interventions
from config.constants import FEATURE_LABELS, RISK_VERDICT

def risk_hint(fname, val):
    if fname == "G2":
        return "🔻" if val <= 10 else "🟢"
    if fname == "grade_trend":
        return "🔻" if val < 0 else ("⚠️" if val == 0 else "🟢")
    if fname == "absences":
        return "🔻" if val >= 10 else "⚪"
    return ""
# ── Load models ───────────────────────────────────────────────────────────────
models = load_models()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div>
    <div class="page-title">Student Risk Prediction</div>
    <div class="page-sub">Two-stage ensemble framework — early screening + confirmation</div>
  </div>
  <div class="header-badges">
    <span class="hbadge">UCI dataset · 395 students</span>
    <span class="hbadge accent">F1 0.88 &nbsp;·&nbsp; AUC 0.911</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
  <strong>How it works:</strong>&nbsp;
  <strong>Stage 1</strong> screens all students using first-term data (G1, demographics, behaviour)
  with Logistic Regression, where the threshold is kept low (p &ge; 0.20) so no at-risk student is missed.
  Students flagged in Stage 1 proceed to <strong>Stage 2</strong>, where a Random Forest + XGBoost
  ensemble uses mid-term data (G2, grade trend) to confirm risk and generate targeted intervention
  recommendations linked to the dominant risk factors.
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INPUT FORM
# ═══════════════════════════════════════════════════════════════════════════════
with st.form("student_form"):

    # ── Academic ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Academic performance</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        G1 = st.number_input("First term grade (G1)", 0, 20, 10)
        st.markdown('<div class="field-note">Scale 0–20. Below 10 = below the passing threshold. Used as a grade trend baseline.</div>', unsafe_allow_html=True)
    with c2:
        G2 = st.number_input("Second term grade (G2)", 0, 20, 10)
        st.markdown('<div class="field-note top">Top predictor of final outcome (importance 0.324). Below 10 triggers a critical tutoring intervention.</div>', unsafe_allow_html=True)
    with c3:
        failures = st.number_input("Past course failures", 0, 4, 0)
        st.markdown('<div class="field-note risk">Number of prior course failures. Each failure compounds risk significantly (importance 0.142).</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Attendance & Engagement ───────────────────────────────────────────────
    st.markdown('<div class="section-label">Attendance and engagement</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4:
        absences = st.number_input("Number of absences", 0, 93, 5)
        st.markdown('<div class="field-note risk">>= 10 absences = high-risk threshold — triggers attendance counseling intervention (importance 0.186).</div>', unsafe_allow_html=True)
    with c5:
        studytime = st.selectbox("Weekly study time", [1, 2, 3, 4],
                                 format_func=lambda x: {
                                     1: "Less than 2 hrs",
                                     2: "2–5 hrs",
                                     3: "5–10 hrs",
                                     4: "More than 10 hrs",
                                 }[x], index=1)
        st.markdown('<div class="field-note">Hours studied per week outside school. Higher values are protective against academic risk.</div>', unsafe_allow_html=True)
    with c6:
        higher = st.selectbox("Aspires to higher education", ["yes", "no"])
        st.markdown('<div class="field-note">Intention to pursue university education. A strong motivational and protective factor.</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Background ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Student background</div>', unsafe_allow_html=True)
    c7, c8, c9 = st.columns(3)
    with c7:
        age = st.number_input("Age", 15, 22, 16)
        st.markdown('<div class="field-note">Typical range 15–17. Age above the norm may indicate grade repetition.</div>', unsafe_allow_html=True)
        sex = st.selectbox("Gender", ["F", "M"],
                           format_func=lambda x: {"F": "Female", "M": "Male"}[x])
        st.markdown('<div class="field-note">Demographic control variable. Not a primary risk driver in this dataset.</div>', unsafe_allow_html=True)
    with c8:
        Medu = st.selectbox("Mother's education level", [0, 1, 2, 3, 4],
                            format_func=lambda x: {
                                0: "None", 1: "Primary (4th grade)",
                                2: "Up to 9th grade", 3: "Secondary", 4: "Higher",
                            }[x], index=2)
        st.markdown('<div class="field-note">0 = none, 4 = higher education. Combined with Fedu as the <em>parent_edu</em> feature.</div>', unsafe_allow_html=True)
        Fedu = st.selectbox("Father's education level", [0, 1, 2, 3, 4],
                            format_func=lambda x: {
                                0: "None", 1: "Primary (4th grade)",
                                2: "Up to 9th grade", 3: "Secondary", 4: "Higher",
                            }[x], index=2)
        st.markdown('<div class="field-note">0 = none, 4 = higher education. Combined with Medu as the <em>parent_edu</em> feature.</div>', unsafe_allow_html=True)
    with c9:
        schoolsup = st.selectbox("School extra support", ["no", "yes"])
        st.markdown('<div class="field-note">Extra tutoring or remedial classes from school. Combined with famsup as <em>support_total</em>.</div>', unsafe_allow_html=True)
        famsup    = st.selectbox("Family educational support", ["yes", "no"])
        st.markdown('<div class="field-note">Educational help at home (homework, private tutoring). Combined with schoolsup as <em>support_total</em>.</div>', unsafe_allow_html=True)

    c10, c11, c12 = st.columns(3)
    with c10:
        address = st.selectbox("Home address type", ["U", "R"],
                               format_func=lambda x: {"U": "Urban", "R": "Rural"}[x])
        st.markdown('<div class="field-note">Urban = better access to learning resources and shorter commute to school.</div>', unsafe_allow_html=True)
    with c11:
        famsize = st.selectbox("Family size", ["GT3", "LE3"],
                               format_func=lambda x: {"GT3": "More than 3", "LE3": "3 or fewer"}[x])
        st.markdown('<div class="field-note">GT3 = more than 3 members, LE3 = 3 or fewer.</div>', unsafe_allow_html=True)
        Pstatus = st.selectbox("Parents living together", ["T", "A"],
                               format_func=lambda x: {"T": "Yes", "A": "No"}[x])
        st.markdown('<div class="field-note">T = living together, A = living apart. Included as a family stability indicator.</div>', unsafe_allow_html=True)
    with c12:
        Mjob = st.selectbox("Mother's job", ["teacher", "health", "services", "at_home", "other"])
        st.markdown('<div class="field-note">at_home = stay-at-home parent; services = civil or public sector employee.</div>', unsafe_allow_html=True)
        Fjob = st.selectbox("Father's job",  ["teacher", "health", "services", "at_home", "other"], index=4)
        st.markdown('<div class="field-note">at_home = stay-at-home parent; services = civil or public sector employee.</div>', unsafe_allow_html=True)

    c13, c14, c15 = st.columns(3)
    with c13:
        reason     = st.selectbox("Reason for school choice", ["course", "home", "reputation", "other"])
        st.markdown('<div class="field-note">course = subject preference, home = proximity, reputation = school prestige.</div>', unsafe_allow_html=True)
        guardian   = st.selectbox("Guardian", ["mother", "father", "other"])
        st.markdown('<div class="field-note">Primary legal guardian and main point of contact for school communications.</div>', unsafe_allow_html=True)
        traveltime = st.selectbox("Travel time to school", [1, 2, 3, 4],
                                  format_func=lambda x: {
                                      1: "Less than 15 min", 2: "15–30 min",
                                      3: "30–60 min",        4: "More than 60 min",
                                  }[x])
        st.markdown('<div class="field-note">Commutes over 30 min can affect fatigue, punctuality, and attendance.</div>', unsafe_allow_html=True)
    with c14:
        activities = st.selectbox("Extra-curricular activities", ["no", "yes"])
        st.markdown('<div class="field-note">Sports, clubs, arts, etc. May reduce study time but can improve engagement.</div>', unsafe_allow_html=True)
        nursery    = st.selectbox("Attended nursery school", ["yes", "no"])
        st.markdown('<div class="field-note">Attended pre-school education. An indicator of early educational investment by the family.</div>', unsafe_allow_html=True)
        internet   = st.selectbox("Internet access at home", ["yes", "no"])
        st.markdown('<div class="field-note">Internet at home is important for homework completion and self-directed study.</div>', unsafe_allow_html=True)
    with c15:
        romantic = st.selectbox("In a romantic relationship", ["no", "yes"])
        st.markdown('<div class="field-note">May affect available study time and overall focus.</div>', unsafe_allow_html=True)
        paid     = st.selectbox("Extra paid classes", ["no", "yes"])
        st.markdown('<div class="field-note">Extra paid tutoring outside school. Indicates academic investment by the family.</div>', unsafe_allow_html=True)
        famrel   = st.slider("Family relationship quality", 1, 5, 4)
        st.markdown('<div class="field-note">1 = very poor, 5 = excellent. Strong family bonds positively correlate with academic performance.</div>', unsafe_allow_html=True)

    c16, c17 = st.columns(2)
    with c16:
        freetime = st.slider("Free time after school", 1, 5, 3)
        st.markdown('<div class="field-note">1 = very low, 5 = very high. Too high may signal low study commitment; too low may indicate burnout risk.</div>', unsafe_allow_html=True)
        goout    = st.slider("Going out with friends",  1, 5, 3)
        st.markdown('<div class="field-note">1 = rarely, 5 = very frequently. High values can reduce available study time.</div>', unsafe_allow_html=True)
    with c17:
        Dalc   = st.slider("Weekday alcohol consumption", 1, 5, 1)
        st.markdown('<div class="field-note risk">1 = none, 5 = very high. High weekday consumption is a behavioural risk indicator affecting attendance and focus.</div>', unsafe_allow_html=True)
        Walc   = st.slider("Weekend alcohol consumption", 1, 5, 2)
        st.markdown('<div class="field-note risk">1 = none, 5 = very high. Assessed together with weekday consumption (Dalc).</div>', unsafe_allow_html=True)
        health = st.slider("Current health status", 1, 5, 3)
        st.markdown('<div class="field-note">1 = very poor, 5 = very good. Poor health directly affects attendance and concentration.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("▶  Run analysis")

# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
if submitted:
    raw = dict(
        sex=sex, age=age, address=address, famsize=famsize,
        Pstatus=Pstatus, Medu=Medu, Fedu=Fedu, Mjob=Mjob, Fjob=Fjob,
        reason=reason, guardian=guardian, traveltime=traveltime,
        studytime=studytime, failures=failures, schoolsup=schoolsup,
        famsup=famsup, paid=paid, activities=activities, nursery=nursery,
        higher=higher, internet=internet, romantic=romantic, famrel=famrel,
        freetime=freetime, goout=goout, Dalc=Dalc, Walc=Walc, health=health,
        absences=absences, G1=G1, G2=G2,
    )

    enc    = build_features(raw, models)
    result = run_prediction(enc, models)

    p1            = result["p1"]
    p2            = result["p2"]
    flagged       = result["flagged"]
    final_risk    = result["final_risk"]
    at_risk       = result["at_risk"]
    stage_reached = result["stage_reached"]
    risk_level    = result["risk_level"]
    risk_label    = result["risk_label"]
    grade_trend   = result["grade_trend"]
    top_feats     = result["top_feats"]
    s1_threshold  = result["stage1_threshold"]

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-header" style="margin-top:0.5rem">
      <div>
        <div class="page-title">Analysis Results</div>
        <div class="page-sub">Two-stage pipeline complete</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric cards ──────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        flag_note = "Flagged → Stage 2" if flagged else "Cleared at Stage 1"
        flag_cls  = "down" if flagged else "up"
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Stage 1 screening</div>
          <div class="metric-value {'danger' if flagged else 'success'}">{p1:.0%}</div>
          <div class="metric-note {flag_cls}">{flag_note}</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        if stage_reached == 2:
            p2_disp  = f"{p2:.0%}"
            p2_note  = "Ensemble confirmed"
            p2_cls   = "danger" if p2 >= 0.5 else "warning"
            note_cls = "down" if p2 >= 0.5 else ""
        else:
            p2_disp  = "—"
            p2_note  = "Stage 2 not triggered"
            p2_cls   = ""
            note_cls = ""
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Stage 2 confirmation</div>
          <div class="metric-value {p2_cls}">{p2_disp}</div>
          <div class="metric-note {note_cls}">{p2_note}</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        t_cls = "danger" if grade_trend < 0 else ("success" if grade_trend > 0 else "")
        n_cls = "down"   if grade_trend < 0 else ("up" if grade_trend > 0 else "")
        n_txt = "Declining" if grade_trend < 0 else ("Improving" if grade_trend > 0 else "Stable")
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Grade trend (G2 − G1)</div>
          <div class="metric-value {t_cls}">{grade_trend:+d}</div>
          <div class="metric-note {n_cls}">{n_txt} performance</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Analysis depth</div>
          <div class="metric-value info">Stage {stage_reached}</div>
          <div class="metric-note">{'Ensemble applied' if stage_reached == 2 else 'Early screening only'}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Verdict + Top features ────────────────────────────────────────────────
    col_v, col_f = st.columns([1, 1])

    with col_v:
        st.markdown(f"""
        <div class="card">
          <div class="section-label">Risk assessment</div>
          <div class="risk-verdict {risk_level}">
            <div class="risk-dot {risk_level}"></div>
            <div>
              <div class="risk-main">{risk_label}</div>
              <div class="risk-sub">{RISK_VERDICT[risk_level]}</div>
            </div>
            <div class="risk-pct {risk_level}">{final_risk:.0%}</div>
          </div>
          <div class="section-label">Analysis pipeline</div>
          <div class="stage-flow">
            <div class="stage-box done">
              <div class="stage-num done">Stage 1</div>
              <div class="stage-title">Early Screening</div>
              <div class="stage-model">Logistic Regression · p &ge; {s1_threshold:.2f}</div>
            </div>
            <span class="stage-arrow">&rsaquo;</span>
            <div class="stage-box {'active' if stage_reached == 2 else ''}">
              <div class="stage-num {'active' if stage_reached == 2 else ''}">Stage 2</div>
              <div class="stage-title">Confirmation</div>
              <div class="stage-model">RF + XGBoost · Soft voting</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_f:
      max_imp = top_feats[0][1] if top_feats else 1

      val_map = {
          "G2": G2,
          "G1": G1,
          "failures": failures,
          "grade_trend": f"{grade_trend:+d}",
          "absences": absences,
          "parent_edu": Medu + Fedu,
      }

      bars_html = ""
      for fname, fimp in top_feats:
          label = FEATURE_LABELS.get(fname, fname)
          val   = val_map.get(fname, "—")

          if fname == "grade_trend":
              hint = risk_hint(fname, grade_trend)
          else:
              hint = risk_hint(fname, val if isinstance(val, (int, float)) else 0)

          bar_w = int((fimp / max_imp) * 100)
          color = "#dc2626" if fimp / max_imp > 0.5 else ("#d97706" if fimp / max_imp > 0.25 else "#6b7280")

          bars_html += (
              f'<div class="pbar-wrap">'
              f'<div class="pbar-row">'
              f'<span class="pbar-name">{label}</span>'
              f'<span class="pbar-val">value: {val} {hint} &nbsp;·&nbsp; {fimp:.3f}</span>'
              f'</div>'
              f'<div class="pbar-bg">'
              f'<div class="pbar-fill" style="width:{bar_w}%;background:{color};"></div>'
              f'</div>'
              f'</div>'
          )

      st.markdown(f"""
      <div class="card" style="height:100%">
        <div class="section-label">Top risk factors (model importance)</div>
        {bars_html}
        <div style="margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid #f3f4f6;font-size:0.72rem;color:#9ca3af;">
          Importance scores from Stage 2 RF + XGBoost ensemble.
        </div>
      </div>
      """, unsafe_allow_html=True)

    # ── Interventions ─────────────────────────────────────────────────────────
    if at_risk or risk_level in ("high", "medium"):
        interventions = build_interventions(result, raw)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="page-header" style="margin-top:0.5rem">
          <div>
            <div class="page-title">Recommended Interventions</div>
            <div class="page-sub">
              Ranked by urgency · Each recommendation is linked to the dominant risk factor
              that triggered it (based on model feature importance, paper Table III)
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        int_html = ""
        for item in interventions:
            int_html += f"""
            <div class="intervention {item['level']}">
              <div class="int-badge {item['level']}">{item['level'].upper()}</div>
              <div class="int-title">{item['title']}</div>
              <div class="int-factor">&#9656; Triggered by: {item['linked_factor']}</div>
              <div class="int-desc">{item['desc']}</div>
            </div>"""
        st.markdown(int_html, unsafe_allow_html=True)

        # ── Guidance office protocol ──────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-label">Guidance office protocol — how to act on this prediction</div>
        <div class="card">
          <div style="font-size:0.8rem;color:#6b7280;margin-bottom:1rem;line-height:1.65;">
            The steps below show how school guidance staff can operationalize EarlyGuard's output
            into a concrete support plan. This protocol is designed to bridge the gap between
            a model prediction and real educational practice.
          </div>
          <div class="protocol-grid">
            <div class="protocol-step">
              <div class="protocol-week">Week 1</div>
              <div class="protocol-action">Flag the student</div>
              <div class="protocol-desc">Notify homeroom teacher and guidance counselor. Share the risk score and dominant factors above.</div>
            </div>
            <div class="protocol-step">
              <div class="protocol-week">Week 2</div>
              <div class="protocol-action">Initial meeting</div>
              <div class="protocol-desc">One-on-one session between counselor and student to understand underlying barriers.</div>
            </div>
            <div class="protocol-step">
              <div class="protocol-week">Week 3</div>
              <div class="protocol-action">Support plan</div>
              <div class="protocol-desc">Design a personalised plan using the interventions above. Enrol student in relevant programmes.</div>
            </div>
            <div class="protocol-step">
              <div class="protocol-week">Monthly</div>
              <div class="protocol-action">Progress review</div>
              <div class="protocol-desc">Re-run EarlyGuard after each assessment cycle. Adjust plan if risk level changes.</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border:1px solid #a7f3d0;
                    border-left:4px solid #059669;border-radius:0 14px 14px 0;padding:1.25rem 1.5rem;margin-top:1.5rem;
                    box-shadow:0 1px 3px rgba(5,150,105,0.08);">
          <div style="font-size:0.92rem;font-weight:700;color:#065f46;margin-bottom:5px;">
            &#10003; No immediate intervention required
          </div>
          <div style="font-size:0.8rem;color:#4b5563;line-height:1.7;">
            This student does not meet the at-risk threshold at this time.
            Continue routine monitoring and re-screen after the next assessment period.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="footer">
      EarlyGuard &nbsp;·&nbsp; ICETT 2026 &nbsp;·&nbsp; Universitas Gadjah Mada<br>
      <span>UCI Student Performance Dataset &nbsp;·&nbsp; Two-stage ensemble framework</span>
    </div>
    """, unsafe_allow_html=True)
