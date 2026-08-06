import time

from tqdm.auto import tqdm
import openai
from Module01_AgenticRAG.rag_helper import RAGBase


def calc_price(usage):
    input_price_per_million = 0.75
    output_price_per_million = 4.50

    input_cost = (usage.input_tokens / 1_000_000) * input_price_per_million
    output_cost = (usage.output_tokens / 1_000_000) * output_price_per_million
    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def calc_total_price(usages):
    total_cost = 0.0

    for usage in usages:
        cost = calc_price(usage)
        total_cost = total_cost + cost["total_cost"]

    return total_cost


def llm_structured(client, instructions, user_prompt, output_type, model="llama-3.3-70b-versatile"):
    messages = [
        {"role": "developer", "content": instructions},
        {"role": "user", "content": user_prompt}
    ]

    response = client.responses.parse(
        model=model,
        input=messages,
        text_format=output_type
    )

    return response.output_parsed, response.usage


def llm_structured_retry(
        client,
        instructions,
        user_prompt,
        output_type,
        model="llama-3.3-70b-versatile",
        max_retries=3,
):
    for attempt in range(max_retries):
        try:
            return llm_structured(
                client,
                instructions,
                user_prompt,
                output_type,
                model=model,
            )
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)


class RAGWithUsage(RAGBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usages = []
        self.last_usage = None

    def reset_usage(self):
        self.usages = []
        self.last_usage = None

    def search(self, query, course=None, num_results=5):
        target_course = course if course else self.course

        boost_dict = {"question": 1.0, "answer": 2.0, "section": 0.1}
        filter_dict = {"course": target_course}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict
        )

    def llm(self, prompt):
        max_retries = 5
        backoff_factor = 2  # Double the sleep time on each failure
        sleep_time = 4      # Start with a 4-second sleep

        for attempt in range(max_retries):
            try:
                response = self.llm_client.responses.create(
                    model=self.model,
                    input=prompt,
                    instructions=self.instructions,
                )

                self.last_usage = response.usage
                self.usages.append(response.usage)
                return response.output_text

            except openai.RateLimitError as e:
                if attempt == max_retries - 1:
                    print("Max retries reached. Failing.")
                    raise e

                print(f"Rate limit hit. Sleeping for {sleep_time}s before retry (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(sleep_time)
                sleep_time *= backoff_factor  # Exponential backoff (4s -> 8s -> 16s...)



        return response.output_text

    def total_cost(self):
        return calc_total_price(self.usages)


def map_progress(pool, seq, f):
    results = []

    with tqdm(total=len(seq)) as progress:
        futures = []

        for el in seq:
            future = pool.submit(f, el)
            future.add_done_callback(lambda p: progress.update())
            futures.append(future)

        for future in futures:
            result = future.result()
            results.append(result)

    return results
