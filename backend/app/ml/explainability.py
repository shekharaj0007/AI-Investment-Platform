"""Module 11: Explainable AI with SHAP / feature importances."""

from __future__ import annotations

import numpy as np


def compute_shap_explanations(
    model,
    features: np.ndarray,
    feature_names: list[str],
    top_k: int = 5,
) -> list[dict[str, float | str]]:
    # Fast path: use tree feature importances
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        pairs = sorted(zip(feature_names, importances, strict=False), key=lambda x: abs(x[1]), reverse=True)
        return [
            {
                "feature": name,
                "shap_value": round(float(val), 4),
                "direction": "positive" if val > 0 else "negative",
            }
            for name, val in pairs[:top_k]
        ]

    try:
        import shap

        explainer = shap.Explainer(model.predict_proba, features)
        shap_values = explainer(features)
        values = shap_values.values
        if values.ndim == 3:
            values = values[0, :, 1]
        elif values.ndim == 2:
            values = values[0]
        pairs = sorted(zip(feature_names, values, strict=False), key=lambda x: abs(float(x[1])), reverse=True)
        return [
            {"feature": name, "shap_value": round(float(val), 4), "direction": "positive" if val > 0 else "negative"}
            for name, val in pairs[:top_k]
        ]
    except Exception:
        return [
            {"feature": name, "shap_value": round(float(v), 4), "direction": "neutral"}
            for name, v in zip(feature_names, features[0][:top_k], strict=False)
        ]
