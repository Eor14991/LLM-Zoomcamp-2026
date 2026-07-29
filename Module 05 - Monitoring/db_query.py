from metrics import  LLMCallRecord
from db_init import get_db_connection

def row_to_record(row):
    return LLMCallRecord(
        model=row[4],
        prompt=row[6],
        instructions=row[5],
        answer=row[2],
        input_tokens=row[7],
        output_tokens=row[8],
        total_tokens=row[9],
        response_time=row[10],
        cost=row[11],
        timestamp=row[12],
    )

def get_conversations(limit = 10):
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, question, answer, course, model,
                       instructions, prompt,
                       prompt_tokens, completion_tokens, total_tokens,
                       response_time, cost, timestamp
                FROM LLMCallRecord
                ORDER BY timestamp DESC
                    LIMIT %s
                """,
                (limit,),
            )
            rows = cursor.fetchall()
    finally:
        conn.close()

    return [row_to_record(row) for row in rows]

if __name__ == "__main__":
    records = get_conversations()
    for record in records:
        print(record)