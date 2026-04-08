"""
utils/model.py
--------------
Cached model loader. Loads model_data.pkl once per Streamlit session.
"""

import os
import pickle
import streamlit as st

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model_data.pkl")

REQUIRED_KEYS = [
    "lr_model", "rf_model", "xgb_model",
    "le_dict", "cat_cols",
    "stage1_features", "stage2_features",
    "stage1_threshold", "feature_importance",
]


@st.cache_resource(show_spinner=False)
def load_models() -> dict:
    """Load and cache trained models and encoders from model_data.pkl."""
    if not os.path.exists(MODEL_PATH):
        st.error(
            "**model_data.pkl not found.**\n\n"
            "Run the training script first to generate the model file:\n"
            "```bash\n"
            "python train.py --data student-mat.csv\n"
            "```\n"
            "Then restart the app.",
            icon="🚫",
        )
        st.stop()

    try:
        with open(MODEL_PATH, "rb") as f:
            data = pickle.load(f)
    except Exception as e:
        st.error(
            f"**Failed to load model_data.pkl:** {e}\n\n"
            "The file may be corrupted. Re-run `python train.py` to regenerate it.",
            icon="🚫",
        )
        st.stop()

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        st.error(
            f"**model_data.pkl is missing required keys:** {missing}\n\n"
            "Re-run `python train.py` to regenerate a compatible model file.",
            icon="🚫",
        )
        st.stop()

    return data
