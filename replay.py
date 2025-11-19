# components/replay.py
import threading
import time
import pandas as pd
import streamlit as st

class ReplaySimulator:
    def __init__(self, model=None, scaler=None, feature_names=None, attack_map=None, alert_cb=None):
        self.model = model
        self.scaler = scaler
        self.feature_names = feature_names
        self.attack_map = attack_map or {}
        self.alert_cb = alert_cb
        self._thread = None
        self._stop = threading.Event()
        self._results = []

    def _map_row(self, row):
        # If the uploaded CSV already has the required features, we just use them.
        X = row[self.feature_names].astype(float).fillna(0).values.reshape(1, -1)
        # scale if scaler provided
        if self.scaler is not None:
            Xs = self.scaler.transform(X)
        else:
            Xs = X
        return Xs

    def _predict_row(self, row):
        try:
            Xs = self._map_row(row)
            pred = self.model.predict(Xs)
            label = self.attack_map.get(int(pred[0]), str(pred[0]))
            return label
        except Exception as e:
            return f"err:{e}"

    def _replay_worker(self, df, delay):
        for idx, row in df.iterrows():
            if self._stop.is_set():
                break
            pred_label = self._predict_row(row) if self.model is not None else "NoModel"
            out = row.to_dict()
            out["predicted_threat"] = pred_label
            out["timestamp"] = pd.Timestamp.now().isoformat()
            self._results.insert(0, out)
            # optional alerting logic: example threshold on label != BENIGN
            try:
                if pred_label != "BENIGN" and self.alert_cb:
                    self.alert_cb(out)
                    # also keep app-level alerts
                    st.session_state.alerts.append({"timestamp": out["timestamp"], "info": pred_label, "row": out})
            except Exception:
                pass
            time.sleep(delay)

    def start_replay(self, df, delay=0.2):
        # clear previous
        self._results = []
        self._stop.clear()
        self._thread = threading.Thread(target=self._replay_worker, args=(df, delay), daemon=True)
        self._thread.start()

    def stop_replay(self):
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)
        self._thread = None

    def get_results(self):
        return self._results
