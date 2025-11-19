# database_manager.py

import sqlite3
import os
from datetime import datetime
import json
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "cyber_data.db")


def init_db():
    """Initialize database and tables."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        # Table to store uploaded file metadata
        cur.execute("""
            CREATE TABLE IF NOT EXISTS file_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER,
                file_name TEXT NOT NULL,
                row_json TEXT,
                uploaded_at TEXT NOT NULL
            )
        """)
        # Table to store chat history
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        # Table to store analysis summaries
        cur.execute("""
            CREATE TABLE IF NOT EXISTS file_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                record_count INTEGER NOT NULL,
                threat_summary TEXT NOT NULL,
                analyzed_at TEXT NOT NULL
            )
        """)
        # Table to store full predictions
        cur.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER NOT NULL,
                predictions_json TEXT NOT NULL,
                saved_at TEXT NOT NULL,
                FOREIGN KEY(file_id) REFERENCES file_summary(id)
            )
        """)
        # Table to store raw CSV/JSON/Parquet uploads (optional)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER NOT NULL,
                raw_json TEXT NOT NULL,
                saved_at TEXT NOT NULL,
                FOREIGN KEY(file_id) REFERENCES file_summary(id)
            )
        """)
        conn.commit()
    print("✅ Database initialized successfully!")


# -------------------------
# File helpers
# -------------------------
def save_file(file_name: str):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO file_data (file_name, uploaded_at) VALUES (?, ?)",
            (file_name, datetime.utcnow().isoformat())
        )
        conn.commit()
        return cur.lastrowid


def get_all_files():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT file_name, uploaded_at FROM file_data ORDER BY uploaded_at DESC"
        )
        return cur.fetchall()


# -------------------------
# File summary helpers
# -------------------------
def save_file_summary(file_name: str, record_count: int, threat_summary: dict):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO file_summary (file_name, record_count, threat_summary, analyzed_at) VALUES (?, ?, ?, ?)",
            (file_name, record_count, json.dumps(threat_summary), datetime.utcnow().isoformat())
        )
        conn.commit()
        return cur.lastrowid


def get_all_file_summaries():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT file_name, record_count, threat_summary, analyzed_at FROM file_summary ORDER BY analyzed_at DESC"
        )
        return cur.fetchall()


# -------------------------
# Predictions helpers
# -------------------------
def save_predictions(file_id: int, df: pd.DataFrame):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO predictions (file_id, predictions_json, saved_at) VALUES (?, ?, ?)",
            (file_id, df.to_json(orient="records"), datetime.utcnow().isoformat())
        )
        conn.commit()


def get_predictions(file_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT predictions_json FROM predictions WHERE file_id=? ORDER BY saved_at DESC",
            (file_id,)
        )
        row = cur.fetchone()
    if row:
        return pd.read_json(row[0], orient="records")
    return pd.DataFrame()


# -------------------------
# Raw CSV/JSON/Parquet data helper
# -------------------------
def save_csv_data(file_id: int, df: pd.DataFrame):
    """Saves raw CSV rows to the database with reference to file_summary id."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        for _, row in df.iterrows():
            cur.execute(
                "INSERT INTO file_data (file_id, file_name, row_json, uploaded_at) VALUES (?, ?, ?, ?)",
                (file_id, getattr(df, "name", "uploaded_file"), row.to_json(), datetime.utcnow().isoformat())
            )
        conn.commit()


def get_csv_data(file_id: int):
    """Retrieve raw data linked to a file summary ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT row_json FROM file_data WHERE file_id=? ORDER BY uploaded_at DESC",
            (file_id,)
        )
        rows = cur.fetchall()
    if rows:
        return pd.DataFrame([json.loads(r[0]) for r in rows])
    return pd.DataFrame()


# -------------------------
# Chat helpers
# -------------------------
def save_chat(file_name: str, role: str, content: str):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (file_name, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (file_name, role, content, datetime.utcnow().isoformat())
        )
        conn.commit()


def get_recent_chats(file_name: str = None, limit: int = 20):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        if file_name:
            cur.execute(
                "SELECT role, content, timestamp FROM chat_history WHERE file_name=? ORDER BY timestamp DESC LIMIT ?",
                (file_name, limit)
            )
        else:
            cur.execute(
                "SELECT role, content, timestamp, file_name FROM chat_history ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
        return cur.fetchall()
