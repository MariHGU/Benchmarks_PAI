import os
# from groq import Groq
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from ollama import Client
from ollama import ChatResponse
import utils  # Assuming you have a function to load your API key

Logger = utils.CustomLogger()


api_key_file = ".api_key.txt"

Logger.info("Init eval model...")
tester_model = utils.GroqModel()
Logger.info("Successful")

Logger.info("Init model...")

model = utils.OllamaLocalModel(
    model="gemma3n:e4b-it-q8_0",
    base_url="https://beta.chat.nhn.no/ollama",
    api_key_file=api_key_file
)

# # Initialize the client with appropriate host and authorization token
# api_key = load_api_key()
# client = Client(
#     host="https://beta.chat.nhn.no/ollama",
#     headers={
#         'Authorization': 'Bearer ' + api_key,
#     }
# )

Logger.info("Successful")



input = """
The 'inclusion score' is calculated as the percentage of assessment questions
for which both the summary and the original document provide a 'yes' answer. This
method ensures that the summary not only includes key information from the original
text but also accurately represents it. A higher inclusion score indicates a
more comprehensive and faithful summary, signifying that the summary effectively
encapsulates the crucial points and details from the original content.
"""

Logger.info("Generating response for input...")

actual_output = model.generate(input)

Logger.info("Response generated successfully.")

# actual_output = client.chat(
#     model="gemma3n:e4b-it-q8_0",
#     messages=[
#         {
#             "role": "user",
#             "content": input,
#         }
#     ],
#     stream=False,
# ).message.content

Logger.info("Creating test case...")

test_case = LLMTestCase(
    input=input,
    actual_output=actual_output,
)

Logger.info("Done.")
Logger.info("Creating metric...")

metric = SummarizationMetric(
    threshold=0.5,
    model=tester_model
)

Logger.info("Done")
Logger.info("Measuring...")

score = metric.measure(test_case)
Logger.info("Done")
print("Score:", score, metric.reason)