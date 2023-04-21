from MT.config import retrivalAPI_IP, retrivalAPI_Port
from typing import Any, List, Dict
import openai
import requests
import logging
import os
import datetime as dt
import openai

DATABASE_INTERFACE_BEAR_TOKEN = os.environ.get("BEARER_TOKEN", None)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

assert DATABASE_INTERFACE_BEAR_TOKEN is not None
assert OPENAI_API_KEY is not None

def query_database(
        query_prompt: str,
        document_id : str = None,
        ) -> Dict[str, Any]:
    """
    Query vector database to retrieve chunk with user's input questions.
    """
    url = f"http://{retrivalAPI_IP}:{retrivalAPI_Port}/query"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {DATABASE_INTERFACE_BEAR_TOKEN}",
    }
    data = {"queries": [{
        "query": query_prompt,
        "filter": {
            "document_id": document_id,
            },
        "top_k": 5}]}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        # process the result
        return result
    else:
        raise ValueError(f"Error: {response.status_code} : {response.content}")


def apply_prompt_template(question: str) -> str:
    """
        A helper function that applies additional template on user's question.
        Prompt engineering could be done here to improve the result. Here I will just use a minimal example.
    """
    prompt = f"""
    You are an assistant who helps people understand academic papers. The most relevant of the known content of the paper has been provided to you. Please answer the following question based on that content: {question}. If you do not think you have enough information to answer the question, please clearly say so.
    """
    return prompt


def call_chatgpt_api(user_question: str, chunks: List[str]) -> Dict[str, Any]:
    """
    Call chatgpt api with user's question and retrieved chunks.
    """
    # Send a request to the GPT-3 API
    messages = list(
        map(lambda chunk: {
            "role": "user",
            "content": chunk
        }, chunks))
    question = apply_prompt_template(user_question)
    messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.7,  # High temperature leads to a more creative response.
    )
    return response


def ask(user_question: str, document_id: str = None) -> Dict[str, Any]:
    """
    Handle user's questions.
    """
    # Get chunks from database.
    chunks_response = query_database(user_question, document_id=document_id)
    chunks = []
    for result in chunks_response["results"]:
        for inner_result in result["results"]:
            chunks.append(inner_result["text"])

    logging.info("User's questions: %s", user_question)
    logging.info("Retrieved chunks: %s", chunks)

    response = call_chatgpt_api(user_question, chunks)
    logging.info("Response: %s", response)

    return response["choices"][0]["message"]["content"]

def direct_ask(questions):
    messageBody = [
            {'role': 'system', 'content': "You are a helpful assistant"},
        ]
    for question in questions:
        messageBody.append({'role': 'user', 'content': question})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messageBody
        )

    return completion['choices'][0]['message']['content']

# TODO : change schema so that there is a categories table and the
#        papers are linked in a many to many relationship to the categories
# TODO : Add a table to the schema to cache the daily category summaries so
#        that we don't have to recompute them every time
