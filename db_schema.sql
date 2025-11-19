CREATE TABLE file_uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    total_records INTEGER,
    threat_summary TEXT,
    uploaded_at TEXT
);

CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    record_index INTEGER,
    threat_type TEXT,
    confidence REAL
);

CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT,
    created_at TEXT
);
