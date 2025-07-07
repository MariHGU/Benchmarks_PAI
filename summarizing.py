import os
import pandas as pd
from typing import List, Tuple
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from ollama import Client, ChatResponse
import utils
from llms import GroqModel, OllamaLocalModel
from llms import MODEL, JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE


def generate_summaries(
        model: str = MODEL, 
        prompts_file: str = "prompts/summarization_prompts.txt",
        api_key_file: str = ".api_key.txt",
        save_file: str = "summaries.csv",
    ) -> None:
    """Generate summaries for a set of prompts using the specified model.

    Args:
        model (str): The model to use for summarization.
        prompts_file (str): The file containing prompts for summarization.
        api_key_file (str): The file containing the API key for the model.
        save_file (str): The file to save the generated summaries to.
    
    Returns:
        None: The function saves the generated summaries to a CSV file.
    """
    Logger = utils.CustomLogger()
    Logger.info("Init model")

    LLM = OllamaLocalModel(
        model=model,
        base_url="https://beta.chat.nhn.no/ollama",
        api_key_file=api_key_file
    )

    Logger.info("Loading prompts from file...")

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    for i, prompt in enumerate(prompts):
        Logger.info("Generating summary for %d. prompt", i + 1)
        response = LLM.generate(prompt)
        utils.write_response_to_csv(
            model_name=model,
            prompt=prompt,
            response=response[0],
            file_name=save_file
        )
    Logger.info("All summaries generated successfully.")


def eval_summaries( 
        api_key_file: str = ".api_key.txt",
        write_results: bool = True,
        result_file: str = "results.xlsx",
        load_file: str = "summaries.csv",
    ) -> List[Tuple[float, str]]:
    """Evaluate the generated summaries using a judge model.
    Args:
        api_key_file (str): The file containing the API key for the judge model.
        write_results (bool): Whether to write the results to a file.
        result_file (str): The file to write the results to.
    Returns:
        List[Tuple[float, str]]: A list of tuples:
            float: The summarization score.
            str: The reasoning for the score explained by the judge model.
    """
    Logger = utils.CustomLogger()
    Logger.info("Init eval model")

    JudgeLLM = OllamaLocalModel(
        model=JUDGE_MODEL,
        base_url="https://beta.chat.nhn.no/ollama",
        api_key_file=api_key_file,
        seed=JUDGE_SEED,
        temperature=JUDGE_TEMPERATURE,
    )

    Logger.info("Preparing metric")
    summarization_metric = SummarizationMetric(
        threshold=0.5,
        model=JudgeLLM
    )

    Logger.info("Successful")
    Logger.info("Loading summaries from CSV file...")

    summaries_df = pd.read_csv(load_file)

    summarization_scores = []
    for i, row in summaries_df.iterrows():
        prompt = row['prompt']
        summary = row['response']
        
        # print("----------------------------")
        # print(f"Prompt {i + 1}: {prompt}")
        # print("_____________")
        # print(f"Summary {i + 1}: {summary}")
        # print("----------------------------")

        Logger.info("Creating test case for %d. prompt", i + 1)
        test_case = LLMTestCase(
            input=prompt,
            actual_output=summary
        )

        Logger.info("Measuring...")
        try:
            summarization_score = summarization_metric.measure(test_case)
        except ValueError as ve:
            Logger.error("Error measuring summarization for prompt %d: %s", i + 1, ve)
            summarization_score = -1.0  # Assign a default score in case of error

        Logger.info("Measurement complete. Score: %s", summarization_score)

        if write_results:
            Logger.info("Writing result to file...")
            utils.save_eval_results_to_xlsx(
                type_of_test="Summarization",
                model_name=row['model'],
                results=[(summarization_score, summarization_metric.reason)],
                file_name=result_file,
                prompt_id=i,
                judge_params=(JudgeLLM.get_model_name(), JudgeLLM.get_seed(), JudgeLLM.get_temperature()),
            )

        summarization_scores.append((summarization_score, summarization_metric.reason))

    Logger.info("All summaries evaluated successfully.")
    return summarization_scores


# def test_summarization(
    #     model: str= MODEL, 
    #     api_key_file: str = ".api_key.txt",
    #     prompts_file: str = "prompts/summarization_prompts.txt",
    #     write_results: bool = True,
    #     result_file: str = "results.xlsx",
    #     ) -> List[tuple]:
    
    # """    Test the summarization model with a given prompt.
    
    # Args:
    #     model (str): The model to use for summarization.
    #     prompts_file (str): The file containing prompts for summarization.
    
    # Returns:
    #     tuple: A tuple containing the score and reason from the metric evaluation.
    # """
    # Logger = utils.CustomLogger()
    # Logger.info("Init eval model")
    
    # # JudgeLLM = GroqModel()
    # JudgeLLM = OllamaLocalModel(
    #     model=JUDGE_MODEL,
    #     base_url="https://beta.chat.nhn.no/ollama",
    #     api_key_file=".api_key.txt",
    #     seed=JUDGE_SEED,
    #     temperature=JUDGE_TEMPERATURE
    # )

    # Logger.info("Init model")

    # LLM = OllamaLocalModel(
    #     model=model,
    #     base_url="https://beta.chat.nhn.no/ollama",
    #     api_key_file=api_key_file
    # )

    # Logger.info("Successful")
    # Logger.info("Loading prompts from file...")

    # with open(prompts_file, "r") as f:
    #     prompts = [line.strip() for line in f if line.strip()]
    
    # summarization_scores = []

    # for i, prompt in enumerate(prompts):
    #     Logger.info("Generating response for %d. prompt", i + 1)
    #     response = LLM.generate(prompt)

    #     # actual_output = client.chat(
    #     #     model="gemma3n:e4b-it-q8_0",
    #     #     messages=[
    #     #         {
    #     #             "role": "user",
    #     #             "content": input,
    #     #         }
    #     #     ],
    #     #     stream=False,
    #     # ).message.content

    #     Logger.info("Creating test case")

    #     test_case = LLMTestCase(
    #         input=prompt,
    #         actual_output=response,
    #     )

    #     Logger.info("Preparing metric")

    #     summarization_metric = SummarizationMetric(
    #         threshold=0.5,
    #         model=JudgeLLM
    #     )

    #     Logger.info("Measuring...")

    #     summarization_score = summarization_metric.measure(test_case)
    #     Logger.info("Measurement complete. Score: %s", summarization_score)

    #     if write_results:
    #         Logger.info("Writing result to file...")

    #         utils.save_eval_results_to_xlsx(
    #             type_of_test="Summarization",
    #             model_name=model,
    #             results=[(summarization_score, summarization_metric.reason)],
    #             file_name=result_file,
    #             prompt_id=i,
    #             judge_params=(JudgeLLM.get_model_name(), JudgeLLM.get_seed(), JudgeLLM.get_temperature()),
    #         )

    #     summarization_scores.append((summarization_score, summarization_metric.reason))

    # return summarization_scores





if __name__ == "__main__":
    # Example usage
    model = "nhn-small:latest"

    prompts_file = "prompts/summarization_prompts.txt"

    # Generate summaries
    # generate_summaries(model=model, prompts_file=prompts_file, save_file="summaries.csv")
    # Evaluate summaries
    results = eval_summaries(api_key_file=".api_key.txt", write_results=True, result_file="results.xlsx", load_file="summaries.csv")

    # results = test_summarization(model=model, prompts_file=prompts_file)
    
    # utils.save_eval_results_to_xlsx(
    #     type_of_test="summarization",
    #     model_name=model,
    #     results=results,
    #     file_name="results.xlsx",
    #     judge_params=(JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE),
    # )