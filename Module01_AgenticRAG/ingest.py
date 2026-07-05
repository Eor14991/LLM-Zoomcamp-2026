import requests
from minsearch import Index

def load_faq_data():
    url = "https://datatalks.club/faq/json/courses.json"
    response = requests.get(url)
    curses_raw = response.json()
    documents = []
    prefix = 'https://datatalks.club/faq'
    for course in curses_raw:
        course_url = f'{prefix}{course["path"]}'

        course_response = requests.get(course_url)
        course_response.raise_for_status()
        curses_raw = course_response.json()

        documents.extend(curses_raw)

    return documents

def built_index(documents):
    index = Index(
        text_fields=["section", "question", "answer"],
        keyword_fields=['course']
    )

    index.fit(documents)

    return index
