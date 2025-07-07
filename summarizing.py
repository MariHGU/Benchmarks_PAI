import os
import pandas as pd
from typing import List, Tuple
from deepeval.metrics import SummarizationMetric, GEval, PromptAlignmentMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from ollama import Client, ChatResponse
import utils
from utils import TestType
from llms import GroqModel, OllamaLocalModel
from llms import MODEL, JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE


def generate_summaries(
        test_type: TestType,
        model: str = MODEL,
        api_key_file: str = ".api_key.txt"
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

    match test_type:
        case TestType.SUMMARIZATION:
            prompts_file = "prompts/summarization_prompts.txt"
            save_file = "responses/summaries.csv"
        case TestType.PROMPT_ALIGNMENT:
            prompts_file = "prompts/alignment_prompts.txt"
            save_file = "responses/alignment_responses.csv"
        case TestType.HELPFULNESS:
            prompts_file = "prompts/helpfulness_prompts.txt"
            save_file = "responses/helpfulness_responses.csv"
        case _:
            raise ValueError("Invalid test type provided. Use TestType.SUMMARIZATION, TestType.PROMPT_ALIGNMENT, or TestType.HELPFULNESS.")
    
    prompts_file = "prompts/summarization_prompts.txt"

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    for i, prompt in enumerate(prompts):
        Logger.info("Generating response for %d. prompt", i + 1)
        response = LLM.generate(prompt)
        time_hash = utils.create_time_hash()
        utils.write_response_to_csv(
            model_name=model,
            prompt=prompt,
            response=response[0],
            file_name=save_file,
            time_hash=time_hash,
            append=i
        )
        utils.write_response_to_csv(
            model_name=model,
            prompt=prompt,
            response=response[0],
            file_name=save_file.replace(".csv", "_archive.csv"),
            time_hash=time_hash
        )
    Logger.info("All summaries generated successfully.")


def eval_summaries( 
        test_type: TestType,
        api_key_file: str = ".api_key.txt",
        write_results: bool = True,
        result_file: str = "results.xlsx"
    ) -> List[Tuple[float, str]]:
    """Evaluate the generated summaries using a judge model.
    Args:
        test_type (TestType): The type of test to perform [].
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

    match test_type:
        case TestType.SUMMARIZATION:
            load_file = "responses/summaries.csv"
            Logger.info("Preparing metric")
            metric = SummarizationMetric(
                threshold=0.5,
                model=JudgeLLM
    )
        case TestType.PROMPT_ALIGNMENT:
            load_file = "responses/alignment_responses.csv"

        case TestType.HELPFULNESS:
            load_file = "responses/helpfulness_responses.csv"
            Logger.info("Preparing metric")
            metric = GEval(
                name="Helpfulness",
                criteria = "Determine whether the `actual output` is helpful in answering the `input`.",
                evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
                model=JudgeLLM
            )

        case _:
            raise ValueError("Invalid test type provided. Use TestType.SUMMARIZATION, TestType.PROMPT_ALIGNMENT, or TestType.HELPFULNESS.")

    Logger.info("Loading responses from CSV file...")

    responses_df = pd.read_csv(load_file)

    scores = []
    for i, row in responses_df.iterrows():
        prompt = row['prompt']
        response = row['response']
        if test_type == TestType.PROMPT_ALIGNMENT:
            Logger.info("Preparing metric for prompt alignment with instructions")
            prompt_instructions = row['prompt_instructions'].split(';') if 'prompt_instructions' in row else [""]
            metric = PromptAlignmentMetric(
                prompt_instructions=prompt_instructions,
                model=JudgeLLM,
                include_reason=True,
            )
  

        Logger.info("Creating test case for %d. prompt", i + 1)
        test_case = LLMTestCase(
            input=prompt,
            actual_output=response
        )

        Logger.info("Measuring...")
        try:
            score = metric.measure(test_case)
        except ValueError as ve:
            Logger.error("Error measuring for prompt %d: %s", i + 1, ve)
            score = -1.0  # Assign a default score in case of error

        Logger.info("Measurement complete. Score: %s", score)

        if write_results:
            Logger.info("Writing result to file...")
            utils.save_eval_results_to_xlsx(
                type_of_test=test_type,
                model_name=row['model'],
                results=[(score, metric.reason)],
                file_name=result_file,
                prompt_id=i,
                judge_params=(JudgeLLM.get_model_name(), JudgeLLM.get_seed(), JudgeLLM.get_temperature()),
                time_hash=row['hash']
            )

        scores.append((score, metric.reason))

    Logger.info("All responses evaluated.")
    return scores


if __name__ == "__main__":
    # Example usage
    model = "nhn-small:latest"

    prompts_file = "prompts/summarization_prompts.txt"

    # Generate summaries
    # generate_summaries(model=model, prompts_file=prompts_file, save_file="summaries.csv")
    # Evaluate summaries
    

    # results = test_summarization(model=model, prompts_file=prompts_file)
    
    # utils.save_eval_results_to_xlsx(
    #     type_of_test="summarization",
    #     model_name=model,
    #     results=results,
    #     file_name="results.xlsx",
    #     judge_params=(JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE),
    # )