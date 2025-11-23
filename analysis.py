"""
Model loading and prediction utilities.
Assumes artifacts are in ./models directory:
- model.joblib (sklearn pipeline)
- explainer.joblib (shap explainer)
- feature_names.joblib (names of transformed features for SHAP plots)
- numerical_cols.joblib (raw numeric input columns)
- categorical_cols.joblib (raw categorical input columns)
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


def load_explainer():
    if os.path.exists(EXPLAINER_PATH):
        return joblib.load(EXPLAINER_PATH)
    return None


def load_feature_names():
    """Names of transformed features used only for SHAP axis labels."""
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
    Build a DataFrame for the model using the raw input feature names
    (numerical + categorical), adding any missing columns with defaults and
    ignoring extra keys (like 'submitted_at').
    """
    df = pd.DataFrame([application_data])

    num_cols = load_numerical_cols() or []
    cat_cols = load_categorical_cols() or []

    # If we know the expected raw columns from training, align to them
    if num_cols or cat_cols:
        expected_cols = list(num_cols) + list(cat_cols)

        # Add missing expected columns with neutral defaults
        for col in expected_cols:
            if col not in df.columns:
                # For simplicity, fill 0 for both numeric and categorical.
                # In your current synthetic setup this is acceptable.
                df[col] = 0

        # Keep only expected columns, in trained order
        df = df[expected_cols]

    # If we do not know the column list (artifacts missing), just use whatever is there.
    return df


# -------------------------
# Prediction
# -------------------------
def predict_proba_and_class(model_pipeline, application_data):
    """
    Returns (probability_of_approval, class)
    class: 1 = approved, 0 = denied
    """
    df = build_input_dataframe(application_data)
    proba = model_pipeline.predict_proba(df)[0, 1]
    pred = int(model_pipeline.predict(df)[0])
    return float(proba), pred


# -------------------------
# SHAP bar plot
# -------------------------
def shap_bar_plot(explainer, model_pipeline, application_data, feature_names=None, topn=10):
    """
    Returns a matplotlib figure with top-n features by absolute SHAP value.

    - Uses explainer already fitted on transformed features.
    - Uses feature_names (transformed feature names) for labels if available.
    """

    # Build raw input DataFrame and transform it
    df = build_input_dataframe(application_data)
    X_trans = model_pipeline.named_steps["preprocessor"].transform(df)

    shap_values = explainer.shap_values(X_trans)

    # shap_values for LinearExplainer often returns array-like (1, n_features)
    arr = shap_values if isinstance(shap_values, (list, tuple)) else [shap_values]
    vals = np.array(arr[0]).flatten()

    if feature_names is None:
        feature_names = load_feature_names()

    if feature_names is None:
        feature_names = [f"f{i}" for i in range(len(vals))]

    # Pair names with SHAP values and sort by absolute importance
    data = list(zip(feature_names, vals))
    data_sorted = sorted(data, key=lambda x: abs(x[1]), reverse=True)[:topn]

    if data_sorted:
        names, values = zip(*data_sorted)
    else:
        names, values = [], []

    # Plot
    fig, ax = plt.subplots(figsize=(6, max(2, len(values) * 0.4)))
    y_pos = range(len(values))
    ax.barh(y_pos, list(values)[::-1])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(names)[::-1])
    ax.set_xlabel("SHAP value")
    ax.set_title("Top SHAP feature contributions")
    plt.tight_layout()
    return fig
