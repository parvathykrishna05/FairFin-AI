"""
Model loading and prediction utilities.
Assumes artifacts are in ./models directory:
- model.joblib        (sklearn pipeline)
- explainer.joblib    (shap explainer on transformed features)
- feature_names.joblib
- numerical_cols.joblib
- categorical_cols.joblib
"""

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import shap
import numpy as np

MODEL_DIR = os.environ.get("MODEL_DIR", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
EXPLAINER_PATH = os.path.join(MODEL_DIR, "explainer.joblib")
FEATURE_NAMES_PATH = os.path.join(MODEL_DIR, "feature_names.joblib")
NUMERICAL_COLS_PATH = os.path.join(MODEL_DIR, "numerical_cols.joblib")
CATEGORICAL_COLS_PATH = os.path.join(MODEL_DIR, "categorical_cols.joblib")


# -------------------------
# Load helpers
# -------------------------
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def load_explainer(model):
    """Create SHAP explainer dynamically instead of loading from disk."""
    try:
        # Get a small synthetic baseline with correct shape
        feature_names = load_feature_names()
        if feature_names is None:
            return None

        background = np.zeros((10, len(feature_names)))  # baseline
        explainer = shap.Explainer(model.predict_proba, background)
        return explainer

    except Exception as e:
        print("SHAP Explainer Error:", e)
        return None



def load_feature_names():
    if os.path.exists(FEATURE_NAMES_PATH):
        return joblib.load(FEATURE_NAMES_PATH)
    return None


def load_numerical_cols():
    if os.path.exists(NUMERICAL_COLS_PATH):
        return joblib.load(NUMERICAL_COLS_PATH)
    return None


def load_categorical_cols():
    if os.path.exists(CATEGORICAL_COLS_PATH):
        return joblib.load(CATEGORICAL_COLS_PATH)
    return None


# -------------------------
# Data alignment helper
# -------------------------
def build_input_dataframe(application_data: dict) -> pd.DataFrame:
    """
    Build a DataFrame for the model using the raw feature names
    (numerical + categorical), adding missing columns with defaults
    and ignoring extras like 'submitted_at'.
    """
    df = pd.DataFrame([application_data])

    num_cols = load_numerical_cols() or []
    cat_cols = load_categorical_cols() or []

    if num_cols or cat_cols:
        expected_cols = list(num_cols) + list(cat_cols)

        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0  # neutral default in your synthetic setup

        df = df[expected_cols]

    return df


# -------------------------
# Prediction
# -------------------------
def predict_proba_and_class(model_pipeline, application_data):
    """Returns (probability_of_approval, predicted_class)."""
    df = build_input_dataframe(application_data)
    proba = model_pipeline.predict_proba(df)[0, 1]
    pred = int(model_pipeline.predict(df)[0])
    return float(proba), pred


# -------------------------
# SHAP bar plot
# -------------------------
def shap_bar_plot(explainer, model_pipeline, application_data, feature_names=None, topn=10):
    """Return a matplotlib figure with top-n features by absolute SHAP value."""
    df = build_input_dataframe(application_data)
    X_trans = model_pipeline.named_steps["preprocessor"].transform(df)

    shap_values = explainer.shap_values(X_trans)
    arr = shap_values if isinstance(shap_values, (list, tuple)) else [shap_values]
    vals = np.array(arr[0]).flatten()

    if feature_names is None:
        feature_names = load_feature_names()
    if feature_names is None:
        feature_names = [f"f{i}" for i in range(len(vals))]

    data = list(zip(feature_names, vals))
    data_sorted = sorted(data, key=lambda x: abs(x[1]), reverse=True)[:topn]

    if data_sorted:
        names, values = zip(*data_sorted)
    else:
        names, values = [], []

    fig, ax = plt.subplots(figsize=(6, max(2, len(values) * 0.4)))
    y_pos = range(len(values))
    ax.barh(y_pos, list(values)[::-1])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(names)[::-1])
    ax.set_xlabel("SHAP value")
    ax.set_title("Top SHAP feature contributions")
    plt.tight_layout()
    return fig


def generate_simple_shap_explanation(explainer, model_pipeline, application_data, feature_names=None, topn=3):
    """
    Generate a human-readable explanation using top SHAP features.
    """
    df = build_input_dataframe(application_data)
    X_trans = model_pipeline.named_steps["preprocessor"].transform(df)

    shap_values = explainer.shap_values(X_trans)
    arr = shap_values if isinstance(shap_values, (list, tuple)) else [shap_values]
    vals = np.array(arr[0]).flatten()

    if feature_names is None:
        feature_names = load_feature_names()
    if feature_names is None:
        feature_names = [f"Feature {i+1}" for i in range(len(vals))]

    pairs = list(zip(feature_names, vals))
    pairs_sorted = sorted(pairs, key=lambda x: abs(x[1]), reverse=True)[:topn]

    if not pairs_sorted:
        return "The model could not generate a clear explanation for this decision."

    lines = []
    for name, value in pairs_sorted:
        human_name = name.replace("_", " ")
        if value < 0:
            lines.append(f"- {human_name} had a negative impact on your loan approval.")
        else:
            lines.append(f"- {human_name} had a positive impact on your loan approval.")

    explanation = "The decision was mainly based on these factors:\n" + "\n".join(lines)
    return explanation
