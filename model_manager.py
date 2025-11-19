# components/model_manager.py
import os
import joblib
import pandas as pd
import streamlit as st
from datetime import datetime

class ModelManager:
    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

    def _list_models(self):
        files = []
        for fname in os.listdir(self.model_dir):
            if fname.endswith((".pkl", ".joblib")):
                files.append(fname)
        return sorted(files)

    def _metadata(self, fname):
        path = os.path.join(self.model_dir, fname)
        stime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
        size_kb = os.path.getsize(path)/1024.0
        algo = "Unknown"
        try:
            mdl = joblib.load(path)
            algo = type(mdl).__name__
        except Exception:
            pass
        return {"file": fname, "modified": stime, "size_kb": f"{size_kb:.1f}", "algo": algo}

    def render(self):
        files = self._list_models()
        uploaded = st.file_uploader("Upload a model (.pkl/.joblib)", type=["pkl", "joblib"])
        if uploaded:
            dest = os.path.join(self.model_dir, uploaded.name)
            with open(dest, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success(f"Saved {uploaded.name} to models/")
            files = self._list_models()
        if files:
            data = [self._metadata(f) for f in files]
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            sel = st.selectbox("Select active model", files, index=0)
            if st.button("Set Active Model"):
                return sel
        else:
            st.info("No models in models/ directory.")
        return None
