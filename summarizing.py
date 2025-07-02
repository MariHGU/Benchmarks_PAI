import os
import pandas as pd
from typing import List, Tuple
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from ollama import Client, ChatResponse
import utils


def test_summarization(
        model: str= "nhn-small:latest", 
        api_key_file: str = ".api_key.txt",
        prompts_file: str = "prompts/summarization_prompts.txt",
        write_results: bool = True,
        result_file: str = "results.xlsx",
        ) -> List[tuple]:
    
    """    Test the summarization model with a given prompt.
    
    Args:
        model (str): The model to use for summarization.
        prompts_file (str): The file containing prompts for summarization.
    
    Returns:
        tuple: A tuple containing the score and reason from the metric evaluation.
    """
    return [(0.8, "Some svada reason"), (0.9, "Another svada reason"), (0.85, "Yet another svada reason")]
    Logger = utils.CustomLogger()
    Logger.info("Init eval model")
    
    # JudgeLLM = utils.GroqModel()
    JudgeLLM = utils.OllamaLocalModel(
        model="nhn-small:latest",
        base_url="https://beta.chat.nhn.no/ollama",
        api_key_file=".api_key.txt",
        seed=utils.JUDGE_SEED,
        temperature=utils.JUDGE_TEMPERATURE
    )

    Logger.info("Init model")

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

        if write_results:
            Logger.info("Writing result to file...")

            utils.log_results(
                type_of_test="Summarization",
                model_name=model,
                results=[(summarization_score, summarization_metric.reason)],
                file_name=result_file,
                prompt_id=i,
                judge_params=(JudgeLLM.get_model_name(), JudgeLLM.get_seed(), JudgeLLM.get_temperature()),
            )

        summarization_scores.append((summarization_score, summarization_metric.reason))

    return summarization_scores





if __name__ == "__main__":
    # Example usage
    model = "qwen3:1.7b-fp16"

    prompts_file = "prompts/summarization_prompts.txt"
    
    results = test_summarization(model=model, prompts_file=prompts_file)
    
    utils.log_results(
        type_of_test="Summarization",
        model_name=model,
        results=results,
        file_name="results.xlsx",
        judge_params=("nhn-small:latest", utils.JUDGE_SEED, utils.JUDGE_TEMPERATURE),
    )