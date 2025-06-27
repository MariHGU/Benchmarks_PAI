import time
import random
from ollama import Client
from ollama import ChatResponse
from utils import load_api_key  # Assuming you have a function to load your API key


api_key = load_api_key()

# Initialize the client with appropriate host and authorization token
client = Client(
    host="https://beta.chat.nhn.no/ollama",
    headers={
        'Authorization': 'Bearer ' + api_key,
    }
)

# Function to call LLM-api
def call_llm_api(prompt):
    try:
        response: ChatResponse = client.chat(model='nhn-small:latest', messages=[{
            'role': 'user',
            'content': prompt,
        }])

        # Extract and return the message content from the response
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            return response.message.content
        else:
            print("Failed to parse message content")
            return None

    except ValueError as e:
        print(f"An error occurred while parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")
        return None

# List of prompts to test the model
prompts = [
    "Hva er værvarselen for i dag?",
    "Fortell meg en historie om en robot.",
    "Hvordan lager jeg pizza?",
    "Hva er differensialregning?",
    "Gi meg en liste over populære programmeringsspråk."
]
# Test LLM performance
def test_llm_performance(prompts, num_tests=5):
    total_time = 0
    for i in range(num_tests):
        prompt = random.choice(prompts)
        start_time = time.time()
        # Call LLM-api
        response = call_llm_api(prompt)
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time

        if response:
            print(f"Test #{i+1}: Prompt='{prompt}' Response='{response[:50]}...' Time={elapsed_time:.4f}s")
        else:
            print(f"Test #{i+1}: Prompt='{prompt}' No response received. Time={elapsed_time:.4f}s")

    average_time = total_time / num_tests
    print(f"\nAverage response time over {num_tests} tests: {average_time:.4f} seconds")
    return average_time

# Run the test
if __name__ == "__main__":
    test_llm_performance(prompts)