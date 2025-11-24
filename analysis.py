"""
Central model + SHAP helper utilities for FairFin
Ensures:
- Safe model loading
- Safe SHAP loading
- Input alignment
- Human readable SHAP explanations
"""

import os
import joblib
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt


# -------------------------
# File paths for artifacts
# -------------------------
MODEL_DIR = os.getenv("MODEL_DIR", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
EXPLAINER_PATH = os.path.join(MODEL_DIR, "explainer.joblib")
FEATURE_NAMES_PATH = os.path.join(MODEL_DIR, "feature_names.joblib")
NUMERICAL_COLS_PATH = os.path.join(MODEL_DIR, "numerical_cols.joblib")
CATEGORICAL_COLS_PATH = os.path.join(MODEL_DIR, "categorical_cols.joblib")


# -------------------------
# Load helpers
# -------------------------
def load_model():
    """Load trained model pipeline"""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def load_explainer():
    """Load SHAP explainer if available"""
    if os.path.exists(EXPLAINER_PATH):
        try:
            return joblib.load(EXPLAINER_PATH)
        except Exception as e:
            print("❌ ERROR loading explainer:", e)
            return None
    return None


def load_feature_names():
    if os.path.exists(FEATURE_NAMES_PATH):
        return joblib.load(FEATURE_NAMES_PATH)
    return None


def load_numerical_cols():
    return joblib.load(NUMERICAL_COLS_PATH) if os.path.exists(NUMERICAL_COLS_PATH) else []


def load_categorical_cols():
    return joblib.load(CATEGORICAL_COLS_PATH) if os.path.exists(CATEGORICAL_COLS_PATH) else []


# -------------------------
# Data alignment
# -------------------------
def build_input_dataframe(application_data: dict) -> pd.DataFrame:
    """
    Convert input JSON into a model-friendly DataFrame and ensure column alignment.
    """

    df = pd.DataFrame([application_data])

    expected_cols = load_numerical_cols() + load_categorical_cols()

    # If model was trained with column list, enforce it
    if expected_cols:
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0  # safe fallback value
        df = df[expected_cols]

    return df


# -------------------------
# Prediction
# -------------------------
def predict_proba_and_class(model_pipeline, application_data):
    """
    Returns tuple: (probability_of_approval, predicted_class)
    """
    df = build_input_dataframe(application_data)
    proba = float(model_pipeline.predict_proba(df)[0, 1])
    pred = int(model_pipeline.predict(df)[0])
    return proba, pred


# -------------------------
# SHAP — Visual Bar Chart
# -------------------------
def shap_bar_plot(explainer, model_pipeline, application_data, feature_names=None, topn=10):

    df = build_input_dataframe(application_data)

    try:
        X_transformed = model_pipeline.named_steps["preprocessor"].transform(df)
        shap_vals = explainer.shap_values(X_transformed)
    except Exception as e:
        raise RuntimeError(f"Unable to generate SHAP values: {e}")

    if isinstance(shap_vals, list):
        shap_vals = shap_vals[0]

    shap_vals = np.array(shap_vals).flatten()

    if feature_names is None:
        feature_names = load_feature_names() or [f"Feature {i}" for i in range(len(shap_vals))]

    paired = list(zip(feature_names, shap_vals))
    sorted_vals = sorted(paired, key=lambda x: abs(x[1]), reverse=True)[:topn]

    names, values = zip(*sorted_vals)
    values = list(values)[::-1]
    names = list(names)[::-1]

    fig, ax = plt.subplots(figsize=(5, len(values) * 0.4 + 1))
    ax.barh(names, values)
    ax.set_title("SHAP Feature Importance")
    ax.set_xlabel("Contribution to Model Decision")
    plt.tight_layout()

    return fig


# -------------------------
# SHAP — Human Explanation
# -------------------------
def generate_simple_shap_explanation(explainer, model_pipeline, application_data, feature_names=None, topn=3):
    """
    Produces human-readable bullet points explaining strongest model influences.
    """

    df = build_input_dataframe(application_data)

    try:
        X_transformed = model_pipeline.named_steps["preprocessor"].transform(df)
        shap_vals = explainer.shap_values(X_transformed)
    except Exception:
        return "The model could not generate an explanation for this decision."

    if isinstance(shap_vals, list):
        shap_vals = shap_vals[0]

    shap_vals = np.array(shap_vals).flatten()

    feature_names = feature_names or load_feature_names() or [f"Feature {i}" for i in range(len(shap_vals))]

    formatted = sorted(list(zip(feature_names, shap_vals)), key=lambda x: abs(x[1]), reverse=True)[:topn]

    explanation = "The decision was influenced most by:\n"
    for name, val in formatted:
        direction = "positive" if val > 0 else "negative"
        clean_name = name.replace("_", " ").capitalize()
        explanation += f"- {clean_name} had a **{direction} impact**\n"

    return explanation.strip()
