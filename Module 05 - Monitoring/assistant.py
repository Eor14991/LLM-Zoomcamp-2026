import sys

from metrics import RAGMetrics
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

    return RAGMetrics(llm_client=openai_client,
                   instructions=INSTRUCTIONS,
                   index=index)

