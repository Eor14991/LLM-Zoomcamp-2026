import sys

from Module01_AgenticRAG.rag_helper import RAGBase
from Module01_AgenticRAG.ingest import load_faq_data, built_index
from openai import OpenAI
import os
from dotenv import load_dotenv


INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()



def create_assistant():
    load_dotenv()
    openai_client = OpenAI(api_key=os.getenv("API_KEY"),
                           base_url=os.getenv("API_URL"))
    documents = load_faq_data()
    index = built_index(documents)

    return RAGBase(llm_client=openai_client,
                   instructions=INSTRUCTIONS,
                   index=index)


if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"
    if len(sys.argv) > 1:
        query = sys.argv[1]

    answer = assistant.rag_pipeline(query)
    print(answer)