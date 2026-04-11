"""
utils/style.py
--------------
Global CSS for EarlyGuard. Injected once from app.py.
Design: modern dashboard — DM Sans + DM Mono, deep navy sidebar, crisp white main,
        indigo/blue gradient accents, elevated cards, smooth transitions.
"""

import streamlit as st


def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ─────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', system-ui, sans-serif;
    font-size: 14px;
}
* { box-sizing: border-box; }

/* ── Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1a1035 100%);
    border-right: 1px solid rgba(99,102,241,0.18);
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] .st-emotion-cache-1cypcdb {
    color: #94a3b8 !important;
    font-size: 0.85rem;
    font-weight: 400;
    letter-spacing: 0.01em;
    transition: color 0.15s ease;
}
[data-testid="stSidebar"] [aria-selected="true"],
[data-testid="stSidebar"] [aria-current="page"] {
    color: #f1f5f9 !important;
    background: rgba(99,102,241,0.18) !important;
    border-radius: 8px !important;
    border-left: 3px solid #818cf8 !important;
}
[data-testid="stSidebar"] a:hover {
    color: #e2e8f0 !important;
}

.sidebar-brand {
    padding: 1.75rem 1.25rem 0.25rem;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #818cf8, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-tagline {
    padding: 0 1.25rem 0.5rem;
    font-size: 0.67rem;
    color: #475569 !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
}
.sidebar-badge {
    display: inline-block;
    margin: 0 1.25rem 1.25rem;
    font-size: 0.67rem;
    padding: 3px 10px;
    border-radius: 20px;
    background: rgba(99,102,241,0.2);
    color: #a5b4fc !important;
    border: 1px solid rgba(99,102,241,0.35);
    letter-spacing: 0.05em;
    font-weight: 600;
}
.sidebar-divider {
    border: none;
    border-top: 1px solid rgba(99,102,241,0.12);
    margin: 0.5rem 1.25rem 0.75rem;
}

/* ── Main area ────────────────────────────────────────────────────────── */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ── Page header ──────────────────────────────────────────────────────── */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    border-bottom: 2px solid #f1f5f9;
    margin-bottom: 1.75rem;
    position: relative;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 56px;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 2px;
}
.page-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.04em;
    line-height: 1.3;
}
.page-sub {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 4px;
    font-weight: 400;
}
.header-badges { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.hbadge {
    font-size: 0.68rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
    background: #f8fafc;
    color: #64748b;
    border: 1px solid #e2e8f0;
    letter-spacing: 0.02em;
    white-space: nowrap;
}
.hbadge.accent {
    background: linear-gradient(135deg, #eff6ff, #eef2ff);
    color: #3730a3;
    border-color: #c7d2fe;
}
.hbadge.success {
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    color: #065f46;
    border-color: #a7f3d0;
}

/* ── Section label ────────────────────────────────────────────────────── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #6366f1;
    margin-bottom: 0.65rem;
}

/* ── Divider ──────────────────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid #f1f5f9;
    margin: 1.75rem 0;
}

/* ── Cards ────────────────────────────────────────────────────────────── */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05);
}
.card-tight {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.875rem 1rem;
}

/* ── Callout ──────────────────────────────────────────────────────────── */
.callout {
    background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%);
    border: 1px solid #bfdbfe;
    border-left: 4px solid #3b82f6;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    font-size: 0.82rem;
    color: #1e3a5f;
    line-height: 1.75;
    margin-bottom: 1.5rem;
}
.callout strong { color: #1d4ed8; }

/* ── Metric cards ─────────────────────────────────────────────────────── */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.125rem 1.25rem 1.125rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.09);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
}
.metric-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.85rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    color: #0f172a;
    line-height: 1.1;
    font-family: 'DM Mono', monospace;
}
.metric-value.danger  { color: #dc2626; }
.metric-value.success { color: #059669; }
.metric-value.warning { color: #d97706; }
.metric-value.info    {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-note {
    font-size: 0.72rem;
    color: #94a3b8;
    margin-top: 0.35rem;
    font-weight: 500;
}
.metric-note.down { color: #dc2626; }
.metric-note.up   { color: #059669; }

/* ── Risk verdict ─────────────────────────────────────────────────────── */
.risk-verdict {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1rem 1.125rem;
    border-radius: 10px;
    margin: 0.65rem 0 1.25rem;
    border: 1px solid transparent;
    border-left: 4px solid transparent;
    transition: transform 0.15s ease;
}
.risk-verdict:hover { transform: translateX(2px); }
.risk-verdict.high   {
    background: linear-gradient(135deg, #fff1f2, #fef2f2);
    border-color: #fca5a5;
    border-left-color: #dc2626;
}
.risk-verdict.medium {
    background: linear-gradient(135deg, #fffbeb, #fef9c3);
    border-color: #fde68a;
    border-left-color: #d97706;
}
.risk-verdict.low    {
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    border-color: #a7f3d0;
    border-left-color: #059669;
}

.risk-dot {
    width: 11px; height: 11px;
    border-radius: 50%;
    flex-shrink: 0;
}
.risk-dot.high   {
    background: #dc2626;
    box-shadow: 0 0 0 4px rgba(220,38,38,0.18);
}
.risk-dot.medium {
    background: #d97706;
    box-shadow: 0 0 0 4px rgba(217,119,6,0.18);
}
.risk-dot.low    {
    background: #059669;
    box-shadow: 0 0 0 4px rgba(5,150,105,0.18);
}

.risk-main {
    font-size: 0.9rem;
    font-weight: 700;
    color: #0f172a;
}
.risk-sub  { font-size: 0.77rem; color: #64748b; margin-top: 2px; line-height: 1.5; }
.risk-pct  {
    margin-left: auto;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    font-family: 'DM Mono', monospace;
}
.risk-pct.high   { color: #dc2626; }
.risk-pct.medium { color: #d97706; }
.risk-pct.low    { color: #059669; }

/* ── Stage flow ───────────────────────────────────────────────────────── */
.stage-flow {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 0.75rem;
    flex-wrap: wrap;
}
.stage-box {
    flex: 1;
    min-width: 100px;
    padding: 0.7rem 0.875rem;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    transition: all 0.15s ease;
}
.stage-box:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.07); }
.stage-box.done   {
    border-color: #a7f3d0;
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
}
.stage-box.active {
    border-color: #c7d2fe;
    background: linear-gradient(135deg, #eff6ff, #eef2ff);
}

.stage-num {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
    margin-bottom: 3px;
}
.stage-num.done   { color: #059669; }
.stage-num.active { color: #4f46e5; }

.stage-title { font-size: 0.78rem; font-weight: 600; color: #0f172a; }
.stage-model { font-size: 0.69rem; color: #94a3b8; margin-top: 2px; }
.stage-arrow { font-size: 1.3rem; color: #cbd5e1; flex-shrink: 0; }

/* ── Progress bars ────────────────────────────────────────────────────── */
.pbar-wrap  { margin-bottom: 0.85rem; }
.pbar-row   { display: flex; justify-content: space-between; margin-bottom: 5px; }
.pbar-name  { font-size: 0.78rem; font-weight: 500; color: #374151; }
.pbar-val   { font-size: 0.72rem; color: #94a3b8; font-family: 'DM Mono', monospace; }
.pbar-bg    { background: #f1f5f9; border-radius: 6px; height: 5px; overflow: hidden; }
.pbar-fill  { height: 100%; border-radius: 6px; transition: width 0.6s cubic-bezier(0.4,0,0.2,1); }

/* ── Intervention cards ───────────────────────────────────────────────── */
.intervention {
    padding: 1.125rem 1.25rem;
    border-radius: 12px;
    margin-bottom: 0.75rem;
    border: 1px solid transparent;
    border-left: 4px solid transparent;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.intervention:hover {
    transform: translateX(4px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.intervention.critical {
    background: linear-gradient(135deg, #fff1f2, #fef2f2);
    border-color: #fecaca;
    border-left-color: #dc2626;
}
.intervention.high {
    background: linear-gradient(135deg, #fffbeb, #fef9c3);
    border-color: #fde68a;
    border-left-color: #d97706;
}
.intervention.moderate {
    background: linear-gradient(135deg, #f0f9ff, #eff6ff);
    border-color: #bae6fd;
    border-left-color: #0284c7;
}

.int-badge {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 20px;
    margin-bottom: 6px;
}
.int-badge.critical { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
.int-badge.high     { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
.int-badge.moderate { background: #e0f2fe; color: #075985; border: 1px solid #bae6fd; }

.int-title  { font-size: 0.86rem; font-weight: 700; color: #0f172a; margin-bottom: 3px; }
.int-factor { font-size: 0.72rem; color: #94a3b8; font-style: italic; margin-bottom: 5px; font-family: 'DM Mono', monospace; }
.int-desc   { font-size: 0.8rem; color: #475569; line-height: 1.7; }

/* ── Protocol timeline ────────────────────────────────────────────────── */
.protocol-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
}
.protocol-step {
    padding: 1.125rem 1rem;
    background: linear-gradient(135deg, #f8fafc, #f1f5f9);
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    text-align: center;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.protocol-step:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.09);
    border-color: #c7d2fe;
}
.protocol-week {
    font-size: 0.63rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6366f1;
    margin-bottom: 5px;
}
.protocol-action {
    font-size: 0.82rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 6px;
}
.protocol-desc {
    font-size: 0.73rem;
    color: #64748b;
    line-height: 1.6;
}

/* ── Paper reference box ──────────────────────────────────────────────── */
.paper-ref {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.875rem 1.125rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    font-size: 0.77rem;
    color: #64748b;
    margin-bottom: 1rem;
}
.paper-ref strong { color: #0f172a; }

/* ── Author cards ─────────────────────────────────────────────────────── */
.author-card {
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.25rem 1.25rem;
    background: #fff;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.author-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(99,102,241,0.12);
    border-color: #c7d2fe;
}
.author-avatar {
    width: 48px; height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #dbeafe, #ede9fe);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 12px;
    font-size: 0.85rem;
    font-weight: 700;
    color: #3730a3;
    border: 2px solid #c7d2fe;
}
.author-name  { font-size: 0.84rem; font-weight: 700; color: #0f172a; }
.author-role  { font-size: 0.7rem;  color: #6366f1;   margin-top: 3px; font-weight: 600; }
.author-dept  { font-size: 0.7rem;  color: #94a3b8;   margin-top: 4px; line-height: 1.5; }
.author-email { font-size: 0.67rem; color: #94a3b8;   margin-top: 5px; font-family: 'DM Mono', monospace; }

/* ── Footer ───────────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    font-size: 0.72rem;
    color: #cbd5e1;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #f1f5f9;
    line-height: 1.9;
}

/* ── Streamlit overrides ──────────────────────────────────────────────── */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
}
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 2.5rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.35) !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(99,102,241,0.45) !important;
}
div[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.3) !important;
}

/* Streamlit slider accent */
div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #6366f1 !important;
    border-color: #6366f1 !important;
}

/* ── Field annotation ─────────────────────────────────────────────────── */
.field-note {
    font-size: 0.7rem;
    color: #94a3b8;
    line-height: 1.5;
    margin-top: -0.35rem;
    margin-bottom: 0.6rem;
    padding-left: 2px;
}
.field-note.risk {
    color: #d97706;
    font-weight: 500;
}
.field-note.top {
    color: #6366f1;
    font-weight: 600;
}

/* Hide Streamlit default top padding / header */
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)
