import os
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from ollama import Client, ChatResponse
import utils


def test_helpfulness(
        model: str= "nhn-small:latest", 
        prompts_file: str = "prompts/helpfulness_prompts.txt",
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
    
    JudgeLLM = utils.GroqModel()

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

        helpfulness_scores.append((helpfulness_score, helpfulness_metric.reason))


    return helpfulness_scores


if __name__ == "__main__":
    # Example usage
    model = "nhn-small:latest"
    prompts_file = "prompts/summarization_prompts.txt"

    results = test_helpfulness(model=model, prompts_file=prompts_file)
    
    for score, reason in results:
        print(f"Score: {score}, Reason: {reason}")