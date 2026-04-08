"""
utils/style.py
--------------
Global CSS for EarlyGuard. Injected once from app.py.
Design: refined academic dashboard — DM Sans + DM Mono, warm slate palette.
"""

import streamlit as st


def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ─────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', system-ui, sans-serif;
    font-size: 14px;
}
* { box-sizing: border-box; }

/* ── Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}
[data-testid="stSidebar"] * { color: #9ca3af !important; }
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] .st-emotion-cache-1cypcdb {
    color: #9ca3af !important;
    font-size: 0.85rem;
    font-weight: 400;
    letter-spacing: 0.01em;
}
[data-testid="stSidebar"] [aria-selected="true"],
[data-testid="stSidebar"] [aria-current="page"] {
    color: #f9fafb !important;
    background: rgba(255,255,255,0.06) !important;
    border-radius: 6px;
}

.sidebar-brand {
    padding: 1.75rem 1.25rem 0.35rem;
    font-size: 1rem;
    font-weight: 600;
    color: #f9fafb !important;
    letter-spacing: -0.03em;
}
.sidebar-tagline {
    padding: 0 1.25rem 0.5rem;
    font-size: 0.68rem;
    color: #4b5563 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}
.sidebar-badge {
    display: inline-block;
    margin: 0 1.25rem 1.25rem;
    font-size: 0.67rem;
    padding: 2px 8px;
    border-radius: 3px;
    background: rgba(59,130,246,0.15);
    color: #60a5fa !important;
    border: 1px solid rgba(59,130,246,0.25);
    letter-spacing: 0.04em;
    font-weight: 500;
}
.sidebar-divider {
    border: none;
    border-top: 1px solid #1f2937;
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
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 1.75rem;
}
.page-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #111827;
    letter-spacing: -0.03em;
    line-height: 1.3;
}
.page-sub {
    font-size: 0.78rem;
    color: #9ca3af;
    margin-top: 3px;
    font-weight: 400;
}
.header-badges { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.hbadge {
    font-size: 0.68rem;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 4px;
    background: #f3f4f6;
    color: #6b7280;
    border: 1px solid #e5e7eb;
    letter-spacing: 0.02em;
    white-space: nowrap;
}
.hbadge.accent {
    background: #eff6ff;
    color: #1d4ed8;
    border-color: #bfdbfe;
}
.hbadge.success {
    background: #f0fdf4;
    color: #15803d;
    border-color: #bbf7d0;
}

/* ── Section label ────────────────────────────────────────────────────── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9ca3af;
    margin-bottom: 0.65rem;
}

/* ── Divider ──────────────────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid #f3f4f6;
    margin: 1.75rem 0;
}

/* ── Cards ────────────────────────────────────────────────────────────── */
.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1.125rem 1.25rem;
    margin-bottom: 0;
}
.card-tight {
    background: #f9fafb;
    border: 1px solid #f3f4f6;
    border-radius: 8px;
    padding: 0.875rem 1rem;
}

/* ── Callout ──────────────────────────────────────────────────────────── */
.callout {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-left: 3px solid #0284c7;
    border-radius: 0 8px 8px 0;
    padding: 0.875rem 1.125rem;
    font-size: 0.82rem;
    color: #0c4a6e;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}
.callout strong { color: #0369a1; }

/* ── Metric cards ─────────────────────────────────────────────────────── */
.metric-card {
    background: #f9fafb;
    border-radius: 10px;
    padding: 1rem 1.125rem;
    border: 1px solid #f3f4f6;
}
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
    margin-bottom: 0.35rem;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 600;
    letter-spacing: -0.04em;
    color: #111827;
    line-height: 1.1;
    font-family: 'DM Mono', monospace;
}
.metric-value.danger  { color: #dc2626; }
.metric-value.success { color: #16a34a; }
.metric-value.warning { color: #d97706; }
.metric-value.info    { color: #2563eb; }
.metric-note {
    font-size: 0.72rem;
    color: #9ca3af;
    margin-top: 0.3rem;
}
.metric-note.down { color: #dc2626; }
.metric-note.up   { color: #16a34a; }

/* ── Risk verdict ─────────────────────────────────────────────────────── */
.risk-verdict {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.875rem 1rem;
    border-radius: 8px;
    margin: 0.65rem 0 1.25rem;
    border: 1px solid transparent;
}
.risk-verdict.high   { background:#fef2f2; border-color:#fecaca; }
.risk-verdict.medium { background:#fffbeb; border-color:#fde68a; }
.risk-verdict.low    { background:#f0fdf4; border-color:#bbf7d0; }

.risk-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.risk-dot.high   { background:#dc2626; box-shadow:0 0 0 3px rgba(220,38,38,0.15); }
.risk-dot.medium { background:#d97706; box-shadow:0 0 0 3px rgba(217,119,6,0.15); }
.risk-dot.low    { background:#16a34a; box-shadow:0 0 0 3px rgba(22,163,74,0.15); }

.risk-main {
    font-size: 0.88rem;
    font-weight: 600;
    color: #111827;
}
.risk-sub  { font-size: 0.77rem; color: #6b7280; margin-top: 2px; line-height: 1.5; }
.risk-pct  {
    margin-left: auto;
    font-size: 1.35rem;
    font-weight: 600;
    letter-spacing: -0.04em;
    font-family: 'DM Mono', monospace;
}
.risk-pct.high   { color: #dc2626; }
.risk-pct.medium { color: #d97706; }
.risk-pct.low    { color: #16a34a; }

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
    padding: 0.6rem 0.75rem;
    border-radius: 7px;
    border: 1px solid #e5e7eb;
    background: #f9fafb;
}
.stage-box.done   { border-color: #bbf7d0; background: #f0fdf4; }
.stage-box.active { border-color: #bfdbfe; background: #eff6ff; }

.stage-num {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
    margin-bottom: 2px;
}
.stage-num.done   { color: #15803d; }
.stage-num.active { color: #1d4ed8; }

.stage-title { font-size: 0.78rem; font-weight: 600; color: #111827; }
.stage-model { font-size: 0.7rem; color: #9ca3af; margin-top: 1px; }
.stage-arrow { font-size: 1.2rem; color: #d1d5db; flex-shrink: 0; }

/* ── Progress bars ────────────────────────────────────────────────────── */
.pbar-wrap  { margin-bottom: 0.75rem; }
.pbar-row   { display: flex; justify-content: space-between; margin-bottom: 4px; }
.pbar-name  { font-size: 0.78rem; font-weight: 500; color: #374151; }
.pbar-val   { font-size: 0.72rem; color: #9ca3af; font-family: 'DM Mono', monospace; }
.pbar-bg    { background: #f3f4f6; border-radius: 3px; height: 4px; overflow: hidden; }
.pbar-fill  { height: 100%; border-radius: 3px; transition: width 0.4s ease; }

/* ── Intervention cards ───────────────────────────────────────────────── */
.intervention {
    padding: 1rem 1.125rem;
    border-radius: 8px;
    margin-bottom: 0.65rem;
    border: 1px solid transparent;
    border-left: 3px solid transparent;
}
.intervention.critical {
    background: #fef2f2;
    border-color: #fecaca;
    border-left-color: #dc2626;
}
.intervention.high {
    background: #fffbeb;
    border-color: #fde68a;
    border-left-color: #d97706;
}
.intervention.moderate {
    background: #f0f9ff;
    border-color: #bae6fd;
    border-left-color: #0284c7;
}

.int-badge {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    padding: 1px 7px;
    border-radius: 3px;
    margin-bottom: 5px;
}
.int-badge.critical { background:#fee2e2; color:#b91c1c; }
.int-badge.high     { background:#fef3c7; color:#92400e; }
.int-badge.moderate { background:#e0f2fe; color:#075985; }

.int-title  { font-size: 0.85rem; font-weight: 600; color: #111827; margin-bottom: 3px; }
.int-factor { font-size: 0.72rem; color: #9ca3af; font-style: italic; margin-bottom: 5px; font-family: 'DM Mono', monospace; }
.int-desc   { font-size: 0.8rem; color: #4b5563; line-height: 1.65; }

/* ── Protocol timeline ────────────────────────────────────────────────── */
.protocol-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
}
.protocol-step {
    padding: 1rem 0.875rem;
    background: #f9fafb;
    border-radius: 8px;
    border: 1px solid #f3f4f6;
    text-align: center;
}
.protocol-week {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #9ca3af;
    margin-bottom: 4px;
}
.protocol-action {
    font-size: 0.8rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 5px;
}
.protocol-desc {
    font-size: 0.72rem;
    color: #6b7280;
    line-height: 1.55;
}

/* ── Paper reference box ──────────────────────────────────────────────── */
.paper-ref {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.75rem 1rem;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 7px;
    font-size: 0.77rem;
    color: #6b7280;
    margin-bottom: 1rem;
}
.paper-ref strong { color: #111827; }

/* ── Author cards ─────────────────────────────────────────────────────── */
.author-card {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1rem 1.125rem;
    background: #fff;
    text-align: center;
}
.author-avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: #f3f4f6;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 10px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #374151;
    border: 1px solid #e5e7eb;
}
.author-name  { font-size: 0.82rem; font-weight: 600; color: #111827; }
.author-role  { font-size: 0.7rem;  color: #2563eb;   margin-top: 2px; font-weight: 500; }
.author-dept  { font-size: 0.7rem;  color: #9ca3af;   margin-top: 3px; line-height: 1.45; }
.author-email { font-size: 0.68rem; color: #9ca3af;   margin-top: 4px; font-family: 'DM Mono', monospace; }

/* ── Footer ───────────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    font-size: 0.72rem;
    color: #d1d5db;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #f3f4f6;
    line-height: 1.8;
}

/* ── Streamlit overrides ──────────────────────────────────────────────── */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
}
div[data-testid="stFormSubmitButton"] > button {
    background: #111827 !important;
    color: #f9fafb !important;
    border: none !important;
    border-radius: 7px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 2rem !important;
    letter-spacing: 0.01em !important;
    transition: background 0.2s !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background: #1f2937 !important;
}
</style>
""", unsafe_allow_html=True)
