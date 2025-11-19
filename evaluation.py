# components/evaluation.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go

class Evaluator:
    def compute_metrics(self, y_true, y_pred, y_prob=None):
        # handle binary/multiclass gracefully
        metrics = {}
        try:
            metrics["accuracy"] = accuracy_score(y_true, y_pred)
            # For multiclass, average='macro'
            metrics["precision"] = precision_score(y_true, y_pred, average='macro', zero_division=0)
            metrics["recall"] = recall_score(y_true, y_pred, average='macro', zero_division=0)
            metrics["f1"] = f1_score(y_true, y_pred, average='macro', zero_division=0)
        except Exception as e:
            st.error(f"Error computing metrics: {e}")
            return {}

        # confusion matrix
        labels = np.unique(np.concatenate([y_true, y_pred]))
        cm = confusion_matrix(y_true, y_pred, labels=labels)
        cm_df = pd.DataFrame(cm, index=labels, columns=labels)

        # confusion plot
        fig_cm = ff.create_annotated_heatmap(
            z=cm_df.values,
            x=[str(x) for x in cm_df.columns],
            y=[str(x) for x in cm_df.index],
            colorscale='Viridis'
        )
        fig_cm.update_layout(title="Confusion Matrix", template="plotly_dark")

        roc_fig = None
        if y_prob is not None and len(np.unique(y_true)) == 2:
            try:
                auc = roc_auc_score(y_true, y_prob)
                fpr, tpr, _ = roc_curve(y_true, y_prob)
                roc_fig = go.Figure()
                roc_fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f"AUC={auc:.3f}"))
                roc_fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines', line=dict(dash='dash'), showlegend=False))
                roc_fig.update_layout(title="ROC Curve", template="plotly_dark", xaxis_title="FPR", yaxis_title="TPR")
            except Exception:
                roc_fig = None

        metrics_table = pd.DataFrame({
            "metric": ["accuracy", "precision (macro)", "recall (macro)", "f1 (macro)"],
            "value": [metrics["accuracy"], metrics["precision"], metrics["recall"], metrics["f1"]]
        })

        return {"metrics_table": metrics_table, "confusion_fig": fig_cm, "roc_fig": roc_fig}

