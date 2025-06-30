import os
# from groq import Groq
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from ollama import Client
from ollama import ChatResponse
import utils  # Assuming you have a function to load your API key


def test_summarization(model: str= "nhn-small:latest", prompts_file: str = "prompts/summarization_prompts.txt") -> list[tuple]:
    """
    Test the summarization model with a given prompt.
    
    Args:
        model (str): The model to use for summarization.
        prompts_file (str): The file containing prompts for summarization.
    
    Returns:
        tuple: A tuple containing the score and reason from the metric evaluation.
    """
    
    Logger = utils.CustomLogger()
    Logger.info("Init eval model...")
    
    JudgeLLM = utils.GroqModel()
    
    Logger.info("Init model...")

    api_key_file = ".api_key.txt"
    LLM = utils.OllamaLocalModel(
        model=model,
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
    Logger.info("Loading prompts from file...")

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    scores = []

    for i, prompt in enumerate(prompts):

        Logger.info("Generating response for %d.prompt", i + 1)

        actual_output = LLM.generate(prompt)

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
            input=prompt,
            actual_output=actual_output,
        )

        Logger.info("Preparing metric...")

        metric = SummarizationMetric(
            threshold=0.5,
            model=JudgeLLM
        )

        Logger.info("Measuring...")

        score = metric.measure(test_case)
        Logger.info("Measurement complete. Score: %s", score.score)

        scores.append((score, metric.reason))

    return scores


if __name__ == "__main__":
    # Example usage
    model = "nhn-small:latest"  # Replace with your model name
    prompts_file = "prompts/summarization_prompts.txt"
    
    results = test_summarization(model=model, prompts_file=prompts_file)
    
    for score, reason in results:
        print(f"Score: {score}, Reason: {reason}")