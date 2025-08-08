import os
from tqdm import tqdm
import pandas as pd
from typing import List, Tuple
from deepeval.metrics import SummarizationMetric, GEval, PromptAlignmentMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from ollama import Client, ChatResponse
import utils
from utils import TypeOfTest
from llms import GroqModel, OllamaLocalModel


def generate_responses(
        test_type: TypeOfTest,
        models: List[str],
        n_responses: int = 1,
    ) -> None:
    """Generate summaries for a set of prompts using the specified model.

    Args:
        test_type (TestType): The type of test to perform, which determines the prompts and save file.
            - TestType.SUMMARIZATION: Generates responses for summarization prompts.
            - TestType.PROMPT_ALIGNMENT: Generates responses for checking prompt alignment.
            - TestType.HELPFULNESS: Generates responses for evaluating helpfulness - the actual output should be helpful in answering the input.
        models (List[str]): A list of model names to use for generating responses.
        n_responses (int): Number of responses to generate for each prompt.

    Returns:
        None: The function saves the generated summaries to a CSV file.
    """
    Logger = utils.CustomLogger()
    _append = False

    for model in models:
        LLM = OllamaLocalModel(model=model)

        Logger.info("Loading prompts from file...")

        match test_type:
            case TypeOfTest.SUMMARIZATION:
                prompts_file = "prompts/summarization_prompts.txt"
                save_file = "responses/summaries.csv"
            case TypeOfTest.PROMPT_ALIGNMENT:
                prompts_file = "prompts/alignment_prompts.txt"
                save_file = "responses/alignment_responses.csv"
            case TypeOfTest.HELPFULNESS:
                prompts_file = "prompts/helpfulness_prompts.txt"
                save_file = "responses/helpfulness_responses.csv"
            case _:
                raise ValueError("Invalid test type provided. Use TestType.SUMMARIZATION, TestType.PROMPT_ALIGNMENT, or TestType.HELPFULNESS.")

        with open(prompts_file, "r") as f:
            prompts = [line.strip() for line in f if line.strip()]

        for i, prompt in enumerate(prompts):
            if test_type == TypeOfTest.PROMPT_ALIGNMENT:
                # For prompt alignment, we need to include the prompt instructions
                prompt_sections = prompt.split("<|INSTRUCTIONS|>")
                if len(prompt_sections) != 2:
                    raise ValueError("prompt/prompt_instructions split failed: expected 2 sections, got {}".format(len(prompt_sections)))

                prompt, prompt_instructions = prompt_sections
                prompt_instructions = prompt_instructions.strip()
            else:
                prompt_instructions = None
            for _ in tqdm(range(n_responses), desc=f"Generating responses for prompt {i}"):
                response = LLM.generate(prompt)
                time_hash = utils.create_time_hash()

                utils.write_response_to_csv(
                    model_name=model,
                    prompt_id=i,
                    prompt=prompt,
                    response=response[0],
                    file_name=save_file,
                    time_hash=time_hash,
                    append=_append, # Remove all old responses when starting a new test
                    prompt_instructions=prompt_instructions
                )
                _append = True  # After the first response, append to the file
                utils.write_response_to_csv(
                    model_name=model,
                    prompt_id=i,
                    prompt=prompt,
                    response=response[0],
                    file_name=save_file.replace(".csv", "_archive.csv"),
                    time_hash=time_hash,
                    prompt_instructions=prompt_instructions
                )
        Logger.info("All generations successful.")


def eval_responses( 
        test_type: TypeOfTest,
        judges: List[Tuple[str, int, float, int]],
        write_results: bool = True,
        result_file: str = "results.xlsx",
        eval_archived: bool = False,
        eval_range: Tuple[int, int] = None,
    ) -> List[Tuple[float, str]]:
    """Evaluate the generated summaries using a judge model.
    Args:
        test_type (TestType): The type of test to perform:
            - TestType.SUMMARIZATION: Evaluates ability to summarize text, and how well the summary captures the main points.
            - TestType.PROMPT_ALIGNMENT: Evaluates how well the model follows the prompt instructions
            - TestType.HELPFULNESS: Evaluates whether the actual output is helpful in answering the input.
        judges (List[Tuple[str, int, float, int]]): A list of tuples containing judge model parameters:
            - str: The name of the judge model
            - int: The seed for the judge model
            - float: The temperature for the judge model
            - int: The top_k for the judge model
        write_results (bool): Whether to write the results to a file.
        result_file (str): The file to write the results to.
        eval_archived (bool): Whether to evaluate all archived responses.
        eval_range (Tuple[int, int]): A tuple specifying the range of responses to evaluate. Deafults to None, which means all responses will be evaluated.
    Returns:
        List[Tuple[float, str]]: A list of tuples:
            float: The summarization score.
            str: The reasoning for the score explained by the judge model.
    """
    Logger = utils.CustomLogger()

    match test_type:
        case TypeOfTest.SUMMARIZATION:
            load_file = "responses/summaries.csv"
        case TypeOfTest.PROMPT_ALIGNMENT:
            load_file = "responses/alignment_responses.csv"
        case TypeOfTest.HELPFULNESS:
            load_file = "responses/helpfulness_responses.csv"
        case _:
            raise ValueError("Invalid test type provided. Use TestType.SUMMARIZATION, TestType.PROMPT_ALIGNMENT, or TestType.HELPFULNESS.")

    if eval_archived:
        load_file = load_file.replace(".csv", "_archive.csv")
    Logger.info("Loading responses from CSV file...")

    responses_df = pd.read_csv(load_file)

    scores = []

    responses = responses_df if not eval_range else responses_df.iloc[eval_range[0]:eval_range[1]]
    for judge in judges:
        Logger.info("Evaluating responses with judge model: %s", judge[0])
        judge_model, judge_seed, judge_temperature, judge_top_k = judge

        for i, row in tqdm(responses.iterrows(), desc="Evaluating responses", total=len(responses)):
            JudgeLLM = OllamaLocalModel(
                model=judge_model,
                seed=judge_seed,
                temperature=judge_temperature,
                top_k=judge_top_k
            )

            match test_type:
                case TypeOfTest.SUMMARIZATION:
                    metric = SummarizationMetric(
                        threshold=0.5,
                        model=JudgeLLM
            )
                case TypeOfTest.PROMPT_ALIGNMENT:
                    prompt_instructions = row['prompt instructions'].split(';') if ';' in row['prompt instructions'] else [row['prompt instructions']]
                    metric = PromptAlignmentMetric(
                        prompt_instructions=prompt_instructions,
                        model=JudgeLLM,
                        include_reason=True,
                    )
                case TypeOfTest.HELPFULNESS:
                    metric = GEval(
                        name="Helpfulness",
                        criteria = "Determine whether the `actual output` is helpful in answering the `input`.",
                        evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
                        model=JudgeLLM
                    )

                case _:
                    raise ValueError("Invalid test type provided. Use TestType.SUMMARIZATION, TestType.PROMPT_ALIGNMENT, or TestType.HELPFULNESS.")
            prompt_id = row['prompt id']
            prompt = row['prompt']
            response = row['response']
    
            Logger.info("Creating test case for prompt %d", i)
            test_case = LLMTestCase(
                input=prompt,
                actual_output=response
            )

            try:
                score = metric.measure(test_case)
            except ValueError as ve:
                Logger.error("Error measuring for prompt %d: %s", i, ve)
                score = -1.0
                metric.reason = "Error in measurement: {}".format(ve)
            except Exception as e:
                Logger.error("Unexpected error for prompt %d: %s", i, e)
                score = -1.0
                metric.reason = "Unexpected error: {}".format(e)

            Logger.info("Evaluation complete. Score: %s", score)

            if write_results:
                utils.save_eval_results_to_xlsx(
                    type_of_test=test_type,
                    model_name=row['model'],
                    results=[(score, metric.reason)],
                    file_name=result_file,
                    judge_params=(judge_model, judge_seed, judge_temperature, judge_top_k),
                    prompt_id=prompt_id,
                    time_hash=row['hash']
                )
                Logger.info("Results saved to %s", result_file)

            scores.append((score, metric.reason))

    Logger.info("All responses evaluated.")
    return scores