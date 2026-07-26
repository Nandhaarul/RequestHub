from app.database.connection import get_connection


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                requester_name TEXT,
                requester_email TEXT,
                source TEXT NOT NULL,
                issue_category TEXT,
                request_text TEXT NOT NULL,
                request_type TEXT NOT NULL,
                urgency TEXT NOT NULL,
                confidence REAL NOT NULL,
                reasoning TEXT NOT NULL,
                status TEXT NOT NULL,
                assigned_team TEXT NOT NULL,
                assigned_agent TEXT,
                assigned_manager TEXT,
                follow_up_at TEXT,
                draft_response TEXT NOT NULL,
                action_summary TEXT NOT NULL,
                review_required INTEGER DEFAULT 0,
                review_reason TEXT,
                current_stage TEXT DEFAULT 'New',
                progress_percent INTEGER DEFAULT 10,
                manager_approval_status TEXT DEFAULT 'Not Required',
                manager_approval_note TEXT,
                override_applied INTEGER DEFAULT 0,
                override_note TEXT
            )
            """
        )
        _add_missing_columns(conn)
        conn.commit()


def _add_missing_columns(conn) -> None:
    existing_columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(cases)").fetchall()
    }

    migrations = {
        "issue_category": "ALTER TABLE cases ADD COLUMN issue_category TEXT",
        "assigned_agent": "ALTER TABLE cases ADD COLUMN assigned_agent TEXT",
        "assigned_manager": "ALTER TABLE cases ADD COLUMN assigned_manager TEXT",
        "review_required": "ALTER TABLE cases ADD COLUMN review_required INTEGER DEFAULT 0",
        "review_reason": "ALTER TABLE cases ADD COLUMN review_reason TEXT",
        "current_stage": "ALTER TABLE cases ADD COLUMN current_stage TEXT DEFAULT 'New'",
        "progress_percent": "ALTER TABLE cases ADD COLUMN progress_percent INTEGER DEFAULT 10",
        "manager_approval_status": "ALTER TABLE cases ADD COLUMN manager_approval_status TEXT DEFAULT 'Not Required'",
        "manager_approval_note": "ALTER TABLE cases ADD COLUMN manager_approval_note TEXT",
        "override_applied": "ALTER TABLE cases ADD COLUMN override_applied INTEGER DEFAULT 0",
        "override_note": "ALTER TABLE cases ADD COLUMN override_note TEXT",
    }

    for column, sql in migrations.items():
        if column not in existing_columns:
            conn.execute(sql)