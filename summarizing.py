import os
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from ollama import Client, ChatResponse
import utils


def test_summarization(
        model: str= "nhn-small:latest", 
        prompts_file: str = "prompts/summarization_prompts.txt"
        ) -> list[tuple]:
    
    """    Test the summarization model with a given prompt.
    
    Args:
        model (str): The model to use for summarization.
        prompts_file (str): The file containing prompts for summarization.
    
    Returns:
        tuple: A tuple containing the score and reason from the metric evaluation.
    """
    
    Logger = utils.CustomLogger()
    Logger.info("Init eval model")
    
    JudgeLLM = utils.GroqModel()
    
    Logger.info("Init model")

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
    
    summarization_scores = []

    for i, prompt in enumerate(prompts):
        Logger.info("Generating response for %d. prompt", i + 1)
        response = LLM.generate(prompt)

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

        Logger.info("Creating test case")

        test_case = LLMTestCase(
            input=prompt,
            actual_output=response,
        )

        Logger.info("Preparing metric")

        summarization_metric = SummarizationMetric(
            threshold=0.5,
            model=JudgeLLM
        )

        Logger.info("Measuring...")

        summarization_score = summarization_metric.measure(test_case)
        Logger.info("Measurement complete. Score: %s", summarization_score)

        summarization_scores.append((summarization_score, summarization_metric.reason))

    return summarization_scores


if __name__ == "__main__":
    # Example usage
    model = "nhn-small:latest"
    prompts_file = "prompts/summarization_prompts.txt"
    
    results = test_summarization(model=model, prompts_file=prompts_file)
    
    for score, reason in results:
        print(f"Score: {score}, Reason: {reason}")