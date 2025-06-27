import time
import random
from ollama import Client
from ollama import ChatResponse
import os

# Initialize the client with appropriate host and authorization token
def get_api_key(file_path='.api_key'):
    try:
        with open(file_path, 'r') as f:
            api_key = f.read().strip()
        return api_key
    except FileNotFoundError:
        print(f"API key file not found: {file_path}")
        raise

# Get the API key from a file outside the git repo
api_key_file = r'C:\Users\mgusdal\OneDrive - Norsk helsenett SF\Skrivebord\Benchmarkin_PAI\.api_key'
api_key = get_api_key(api_key_file)

client = Client(
    host="https://chat.nhn.no/ollama",
    headers={
        'Authorization': f'{api_key}'
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
    "Hva er differensiallikning?",
    "Hvem er presidenten i usa?",
    "Gi meg en liste over populære programmeringsspråk."
]

# Test LLM performance
def test_llm_performance(prompts, num_tests=6):
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