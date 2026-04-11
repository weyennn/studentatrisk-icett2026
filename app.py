"""
app.py
------
EarlyGuard — Streamlit entry point.
Configures page, injects global CSS, and registers the navigation pages.
"""

import os
import streamlit as st

_LOGO = os.path.join(os.path.dirname(__file__), "assets", "logo.svg")

st.set_page_config(
    page_title="EarlyGuard",
    page_icon=_LOGO if os.path.exists(_LOGO) else "🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.style import inject_css
inject_css()

# ── Sidebar branding ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div class="sidebar-brand">
  <span style="-webkit-text-fill-color:transparent;background:linear-gradient(135deg,#818cf8,#38bdf8);-webkit-background-clip:text;">&#9673; EarlyGuard</span>
</div>""", unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-tagline">At-Risk Student Detection</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<span class="sidebar-badge">&#9733; ICETT 2026 &middot; UGM</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

# ── Navigation ─────────────────────────────────────────────────────────────────
pg = st.navigation([
    st.Page("pages/predict.py",  title="Prediction",  url_path="predict",  default=True),
    st.Page("pages/overview.py", title="Overview",    url_path="overview"),
    st.Page("pages/about.py",    title="About",       url_path="about"),
])
pg.run()
