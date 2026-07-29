import os
from datetime import datetime, timezone
import psycopg

DB_TIMEZONE = timezone.utc
print(f'Using timezone: {DB_TIMEZONE}')

def get_db_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        dbname=os.getenv("POSTGRES_DB", "course_assistant"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
    )

def init_db(drop = False):
    conn = get_db_connection()
    try:
        with conn.cursor() as curs:
            if drop:
                curs.execute("DROP TABLE IF EXISTS LLMCallRecord")

            curs.execute("\n".join([
                "CREATE TABLE IF NOT EXISTS LLMCallRecord (",
                "    id SERIAL PRIMARY KEY,",
                "    question TEXT NOT NULL,",
                "    answer TEXT NOT NULL,",
                "    course TEXT NOT NULL,",
                "    model TEXT NOT NULL,",
                "    instructions TEXT NOT NULL,",
                "    prompt TEXT NOT NULL,",
                "    prompt_tokens INTEGER NOT NULL,",
                "    completion_tokens INTEGER NOT NULL,",
                "    total_tokens INTEGER NOT NULL,",
                "    response_time FLOAT NOT NULL,",
                "    cost FLOAT NOT NULL,",
                "    timestamp TIMESTAMP WITH TIME ZONE NOT NULL",
                ")"
            ]))

            conn.commit()

    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized")