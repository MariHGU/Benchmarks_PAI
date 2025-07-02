import os
from deepeval.metrics import PromptAlignmentMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from ollama import Client, ChatResponse
import utils


def test_prompt_alignment(
        model: str = "nhn-small:latest", 
        prompts_file: str = "prompts/alignment_prompts.txt",
        prompt_instructions: list[str] = [""],
    ) -> list[tuple]:

    """    Test the prompt alignment model with a given prompt.

    Args:
        model (str): The model to use for alignment.
        prompts_file (str): The file containing prompts for alignment.
        prompt_instructions (list[str]): Instructions for the prompt alignment metric.
    Returns:
        list[tuple]: A list of tuples containing the alignment score and reason for each prompt.
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

    Logger.info("Preparing metric...")

    prompt_alignment_metric= PromptAlignmentMetric(
        prompt_instructions= prompt_instructions,
        model=JudgeLLM,
        include_reason=True,
    )

    Logger.info("Successful")
    Logger.info("Loading prompts from file...")

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    alignment_scores = []

    for i, prompt in enumerate(prompts):
        Logger.info("Generating response for prompt %d", i + 1)
        response = LLM.generate(prompt)

        Logger.info("Creating test case")
        test_case = LLMTestCase(
            input=prompt,
            actual_output=response,
        )
        Logger.info("Measuring...")
        alignment_score = prompt_alignment_metric.measure(test_case)

        Logger.info("Score for prompt %d: %s", i + 1, alignment_score)
        Logger.info("Reason: %s", prompt_alignment_metric.reason)

        alignment_scores.append((alignment_score, prompt_alignment_metric.reason))

    return alignment_scores


if __name__ == "__main__":
    # Example usage
    model = "nhn-small:latest"
    prompts_file = "prompts/summarization_prompts.txt"
    
    results = test_prompt_alignment(model=model, prompts_file=prompts_file, prompt_instructions=["Reply in all uppercase", "Reply", "Respond with a summary"])
    
    for score, reason in results:
        print(f"Score: {score}, Reason: {reason}")