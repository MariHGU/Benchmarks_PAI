import os
from groq import Groq
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from ollama import Client
from ollama import ChatResponse
from utils import load_api_key, OllamaLocalModel  # Assuming you have a function to load your API key

print("loading API key...")

api_key_file = ".api_key.txt"
api_key = load_api_key()

print("initializing judge...")

judge = OllamaLocalModel(
    model="gemma3n:e4b-it-q8_0",
    base_url="https://beta.chat.nhn.no/ollama",
    api_key_file=api_key_file,
)

print("initializing client...")

# Initialize the client with appropriate host and authorization token
client = Client(
    host="https://beta.chat.nhn.no/ollama",
    headers={
        'Authorization': 'Bearer ' + api_key,
    }
)

print("client initialized successfully.")

# # Function to call LLM-api
# def call_llm_api(prompt):
#     try:
#         response: ChatResponse = client.chat(model='nhn-small:latest', messages=[{
#             'role': 'user',
#             'content': prompt,
#         }])

#         # Extract and return the message content from the response
#         if hasattr(response, 'message') and hasattr(response.message, 'content'):
#             return response.message.content
#         else:
#             print("Failed to parse message content")
#             return None

#     except ValueError as e:
#         print(f"An error occurred while parsing JSON: {e}")
#         return None
#     except Exception as e:
#         print(f"An error occurred while calling the API: {e}")
#         return None
    

# class BetaLLM(DeepEvalBaseLLM):
#     def __init__(self, model_name: str):
#         super().__init__(model_name=model_name)

#     def chat(self, messages):
#         prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
#         response = call_llm_api(prompt)
#         return response



# print("setting up environment...")
# groq_api_key = "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"
# print("initializing Groq client...")
# client = Groq(api_key=groq_api_key)
# chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Explain the concept of large language models.",
#             }
#         ],
#         model="llama-3.1-8b-instant",  # Or another desired Groq model
#     )

# print("------------------------------")
# print("Chat completion response:")
# print(chat_completion.choices[0].message.content)
# print("------------------------------")



# print("Groq client initialized successfully.")

input = """
The 'inclusion score' is calculated as the percentage of assessment questions
for which both the summary and the original document provide a 'yes' answer. This
method ensures that the summary not only includes key information from the original
text but also accurately represents it. A higher inclusion score indicates a
more comprehensive and faithful summary, signifying that the summary effectively
encapsulates the crucial points and details from the original content.
"""

actual_output = """
The inclusion score quantifies how well a summary captures and
accurately represents key information from the original text,
with a higher score indicating greater comprehensiveness.
"""
print("creating test case...")

test_case = LLMTestCase(
    input=input,
    actual_output=actual_output,
)

print("creating metric...")

metric = SummarizationMetric(
    threshold=0.5,
    model=judge
)

print("measuring...")

score = metric.measure(test_case)
print("score:", score, metric.reason)