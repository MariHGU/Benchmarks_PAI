import os
from deepeval.metrics import PromptAlignmentMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from ollama import Client, ChatResponse
import utils
from utils import MODEL, JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE


def test_prompt_alignment(
        model: str = MODEL,
        prompts_file: str = "prompts/alignment_prompts.txt",
        prompt_instructions: list[str] = [""],
        write_results: bool = True,
        result_file: str = "results.xlsx",
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

        if write_results:
            Logger.info("Writing result to file...")

            utils.log_results(
                type_of_test="Prompt Alignment",
                model_name=model,
                results=[(alignment_score, prompt_alignment_metric.reason)],
                file_name=result_file,
                prompt_id=i,
                judge_params=(JudgeLLM.get_model_name(), JudgeLLM.get_seed(), JudgeLLM.get_temperature()),
            )

        alignment_scores.append((alignment_score, prompt_alignment_metric.reason))

    return alignment_scores


if __name__ == "__main__":
    # Example usage
    model = MODEL
    prompts_file = "prompts/summarization_prompts.txt"
    
    results = test_prompt_alignment(
                        model=model,
                        prompts_file=prompts_file, 
                        prompt_instructions=[
                            "Reply in all uppercase", 
                            "Reply", 
                            "Respond with a summary"
                            ],
                        write_results=True,
                        result_file="results.xlsx"
                        )
    
    # utils.log_results(
    #     type_of_test="prompt alignment",
    #     model_name=model,
    #     results=results,
    #     file_name="results.xlsx",
    #     judge_params=(JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE),
    # )