class RAGBase:
    def __init__(self,
                 index,
                 llm_client,
                 instructions:str,
                 course="llm-zoomcamp",
                 model="llama-3.3-70b-versatile"):
        self.instructions = instructions
        self.index = index
        self.llm_client = llm_client
        self.course = course
        self.model = model

    def search(self, query: str, course: str):
        return self.index.search(
            query=query,
            filter_dict={'course': course},
            num_results=5
        )

    def llm(self, prompt):
        response = self.llm_client.responses.create(
            input=prompt,
            model=self.model,
        )
        return response.output_text

    def rag_pipeline(self, query: str, course=None):
        if course is None:
            course = self.course

        search_result = self.search(query, course)
        context = self.build_context(search_result)
        system_message_ = self.system_message(context)

        prompt = self.prompt_builder(query, system_message_)

        answer = self.llm(prompt)
        return answer

    def prompt_builder(self, query, system_message):
        return [
            {'role': "system", "content": system_message},
            {'role': "user", "content": query}
        ]

    def system_message(self, context):
        # Cleaned up the formatting for a cleaner system prompt
        return self.instructions+f"{context}"

    def build_context(self, search_result):
        lines = []
        for docs in search_result:
            lines.append(docs['section'])
            lines.append("Q: " + docs['question'])
            lines.append("A: " + docs['answer'])
            lines.append('')
        return "\n".join(lines).strip()