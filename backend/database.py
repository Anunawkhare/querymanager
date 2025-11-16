import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()

    # Queries table
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            customer_email TEXT,
            subject TEXT,
            content TEXT NOT NULL,
            category TEXT,
            priority INTEGER DEFAULT 1,
            status TEXT DEFAULT 'new',
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Teams table
    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            categories TEXT,  # JSON array of categories they handle
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    # Response history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id INTEGER,
            agent_id TEXT,
            response_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (query_id) REFERENCES queries (id)
        )
    ''')

    # Insert sample teams
    sample_teams = [
        ('Support Team', 'support@company.com', '["question","technical"]'),
        ('Billing Team', 'billing@company.com', '["billing","payment"]'),
        ('Complaints Team', 'complaints@company.com', '["complaint","urgent"]')
    ]

    c.executemany('''
        INSERT OR IGNORE INTO teams (name, email, categories)
        VALUES (?, ?, ?)
    ''', sample_teams)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def get_db_connection():
    conn = sqlite3.connect('queries.db')
    conn.row_factory = sqlite3.Row
    return conn