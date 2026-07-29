import json
from datetime import datetime
from db_init import get_db_connection, DB_TIMEZONE


def save_conversation(record, question, course):
    timestamp = datetime.now(DB_TIMEZONE)

    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO LLMCallRecord (
                question, answer, course, model, instructions, prompt,
                prompt_tokens, completion_tokens, total_tokens,
                response_time, cost, timestamp
            ) VALUES (
                         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                     )
                RETURNING id
            """,
            (
                question,
                record.answer,
                course,
                record.model,
                record.instructions,
                json.dumps(record.prompt),
                record.input_tokens,
                record.output_tokens,
                record.total_tokens,
                record.response_time,
                record.cost,
                timestamp,
            ),

        )
        conversation_id = cursor.fetchone()[0]
        conn.commit()
    finally:
        conn.close()
    return conversation_id
