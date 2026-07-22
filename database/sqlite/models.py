from __future__ import annotations


class DatabaseModels:
    """
    Contains SQL statements for creating the application's database tables.
    """

    CREATE_CONVERSATIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_query TEXT NOT NULL,
        assistant_response TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """

    CREATE_KNOWLEDGE_DOCUMENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS knowledge_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_name TEXT NOT NULL,
        document_path TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """

    CREATE_FEEDBACK_TABLE = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comments TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (conversation_id)
            REFERENCES conversations(id)
            ON DELETE CASCADE
    );
    """

    TABLES = (
        CREATE_CONVERSATIONS_TABLE,
        CREATE_KNOWLEDGE_DOCUMENTS_TABLE,
        CREATE_FEEDBACK_TABLE,
    )