import os
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from ollama import Client, ChatResponse
import utils
from utils import MODEL, JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE


def test_helpfulness(
        model: str= MODEL, 
        prompts_file: str = "prompts/helpfulness_prompts.txt",
        write_results: bool = True,
        result_file: str = "results.xlsx",
        ) -> list[tuple]:
    
    """    Test whether the model's output is giving a correct and helpful type of response to the given prompt.

    Args:
        model (str): The model to use for evaluation.
        prompts_file (str): The file containing prompts for evaluation.
    Returns:
        list[tuple]: A list of tuples containing the helpfulness score and reason for each prompt.
    """

    Logger = utils.CustomLogger()
    Logger.info("Init eval model")
    
    # JudgeLLM = utils.GroqModel()
    JudgeLLM = utils.OllamaLocalModel(
        model=JUDGE_MODEL,
        base_url="https://beta.chat.nhn.no/ollama",
        api_key_file=".api_key.txt",
        seed=JUDGE_SEED,
        temperature=JUDGE_TEMPERATURE
    )

    Logger.info("Init model")

    api_key_file = ".api_key.txt"
    LLM = utils.OllamaLocalModel(
        model=model,
        base_url="https://beta.chat.nhn.no/ollama",
        api_key_file=api_key_file
    )

    Logger.info("Preparing metric")

    helpfulness_metric = GEval(
        name="Helpfulness",
        criteria = "Determine whether the `actual output` is helpful in answering the `input`.",
        evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=JudgeLLM
    )

    Logger.info("Successful")
    Logger.info("Loading prompts from file...")

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    helpfulness_scores = []

    for i, prompt in enumerate(prompts):
        Logger.info("Generating response for prompt %d", i + 1)
        response = LLM.generate(prompt)

        Logger.info("Creating test case")
        test_case = LLMTestCase(
            input=prompt,
            actual_output=response,
        )
        Logger.info("Measuring...")
        helpfulness_score = helpfulness_metric.measure(test_case)

        Logger.info("Score for prompt %d: %s", i + 1, helpfulness_score)
        Logger.info("Reason: %s", helpfulness_metric.reason)

        if write_results:
            Logger.info("Writing result to file...")

            utils.log_results(
                type_of_test="Helpfulness",
                model_name=model,
                results=[(helpfulness_score, helpfulness_metric.reason)],
                file_name=result_file,
                prompt_id=i,
                judge_params=(JudgeLLM.get_model_name(), JudgeLLM.get_seed(), JudgeLLM.get_temperature()),
            )


        helpfulness_scores.append((helpfulness_score, helpfulness_metric.reason))


    return helpfulness_scores


if __name__ == "__main__":
    # Example usage
    model = "nhn-small:latest"
    prompts_file = "prompts/summarization_prompts.txt"

    results = test_helpfulness(model=model, prompts_file=prompts_file)
    
    # utils.log_results(
    #     type_of_test="helpfulness",
    #     model_name=model,
    #     results=results,
    #     file_name="results.xlsx",
    #     judge_params=(JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE),
    # )