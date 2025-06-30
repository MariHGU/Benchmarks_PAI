from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
import utils


def test_helpfulness(model: str= "nhn-small:latest", prompts_file: str = "prompts/summarization_prompts.txt") -> list[tuple]:

    Logger = utils.CustomLogger()
    Logger.info("Init eval model...")
    
    JudgeLLM = utils.GroqModel()

    Logger.info("Init model...")

    api_key_file = ".api_key.txt"
    LLM = utils.OllamaLocalModel(
        model=model,
        base_url="https://beta.chat.nhn.no/ollama",
        api_key_file=api_key_file
    )

    Logger.info("Preparing metric...")

    helpfulness_metric = GEval(
        name="Helpfulness",
        criteria = "Determine whether the `actual output` is helpful in answering the `input`.",
        evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=JudgeLLM
    )

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    helpfulness_scores = []

    for i, prompt in enumerate(prompts):
        Logger.info("Generating response for prompt %d", i + 1)
        response = LLM.generate(prompt)

        Logger.info("Creating test case...")
        test_case = LLMTestCase(
            input=prompt,
            actual_output=response,
        )
        Logger.info("Measuring...")
        helpfulness_score = helpfulness_metric.evaluate(test_case)

        Logger.info("Score for prompt %d: %s", i + 1, helpfulness_score.score)
        Logger.info("Reason: %s", helpfulness_score.reason)

        helpfulness_scores.append((helpfulness_score, helpfulness_metric.reason))