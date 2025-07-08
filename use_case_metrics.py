import os
from tqdm import tqdm
import pandas as pd
from typing import List, Tuple
from deepeval.metrics import SummarizationMetric, GEval, PromptAlignmentMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from ollama import Client, ChatResponse
import utils
from utils import TestType
from llms import GroqModel, OllamaLocalModel
from llms import MODEL, JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE


def generate_responses(
        test_type: TestType,
        model: str = MODEL,
        n_responses: int = 1,
    ) -> None:
    """Generate summaries for a set of prompts using the specified model.

    Args:
        test_type (TestType): The type of test to perform, which determines the prompts and save file.
            - TestType.SUMMARIZATION: Generates responses for summarization prompts.
            - TestType.PROMPT_ALIGNMENT: Generates responses for checking prompt alignment.
            - TestType.HELPFULNESS: Generates responses for evaluating helpfulness - the actual output should be helpful in answering the input.
        model (str): Name of the model to use for generating summaries.
        n_responses (int): Number of responses to generate for each prompt.
    
    Returns:
        None: The function saves the generated summaries to a CSV file.
    """

    Logger = utils.CustomLogger()
    Logger.info("Init model")

    LLM = OllamaLocalModel(model=model)

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

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    for i, prompt in enumerate(prompts):
        Logger.info("Generating %d response(s) for %d. prompt" %(n_responses, i + 1))
        if test_type == TestType.PROMPT_ALIGNMENT:
            # For prompt alignment, we need to include the prompt instructions
            prompt_sections = prompt.split("<|INSTRUCTIONS|>")
            if len(prompt_sections) != 2:
                raise ValueError("prompt/prompt_instructions split failed: expected 2 sections, got {}".format(len(prompt_sections)))

            prompt, prompt_instructions = prompt_sections
            prompt_instructions = prompt_instructions.strip()
        else:
            prompt_instructions = None
        for _ in tqdm(range(n_responses)):
            response = LLM.generate(prompt)
            time_hash = utils.create_time_hash()

            utils.write_response_to_csv(
                model_name=model,
                prompt=prompt,
                response=response[0],
                file_name=save_file,
                time_hash=time_hash,
                append=i, # Remove all old responses when starting a new test
                prompt_instructions=prompt_instructions
            )
            utils.write_response_to_csv(
                model_name=model,
                prompt=prompt,
                response=response[0],
                file_name=save_file.replace(".csv", "_archive.csv"),
                time_hash=time_hash,
                prompt_instructions=prompt_instructions
            )
    Logger.info("All generations successful.")


def eval_responses( 
        test_type: TestType,
        write_results: bool = True,
        result_file: str = "results.xlsx",
        eval_archived: bool = False,
    ) -> List[Tuple[float, str]]:
    """Evaluate the generated summaries using a judge model.
    Args:
        test_type (TestType): The type of test to perform:
            - TestType.SUMMARIZATION: Evaluates ability to summarize text, and how well the summary captures the main points.
            - TestType.PROMPT_ALIGNMENT: Evaluates how well the model follows the prompt instructions
            - TestType.HELPFULNESS: Evaluates whether the actual output is helpful in answering the input.
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


    if eval_archived:
        load_file = load_file.replace(".csv", "_archive.csv")
    Logger.info("Loading responses from CSV file...")

    responses_df = pd.read_csv(load_file)

    scores = []
    for i, row in tqdm(responses_df.iterrows()):
        prompt = row['prompt']
        response = row['response']
        if test_type == TestType.PROMPT_ALIGNMENT:
            Logger.info("Preparing metric for prompt alignment with instructions")
            prompt_instructions = row['prompt instructions'].split(';') if ';' in row['prompt instructions'] else [row['prompt instructions']]
            print("Prompt instructions:", prompt_instructions)
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
    # generate_responses(model=model, prompts_file=prompts_file, save_file="summaries.csv")
    # Evaluate summaries
    

    # results = test_summarization(model=model, prompts_file=prompts_file)
    
    # utils.save_eval_results_to_xlsx(
    #     type_of_test="summarization",
    #     model_name=model,
    #     results=results,
    #     file_name="results.xlsx",
    #     judge_params=(JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE),
    # )