import asyncio
from benchmarking import initBenchmarking
from use_case_metrics import generate_responses, eval_responses
from utils import TestType

JUDGE_MODEL1 = "nhn-large:latest" # "qwen3-coder:30b-a3b-q8_0" # OLLAMA
JUDGE_MODEL2 = "nhn-medium:latest" # "devstral:24b-small-2505-fp16" # OLLAMA
JUDGE_MODEL3 = "hermes3:70b-llama3.1-fp16" # OLLAMA
JUDGE_SEED = 42
JUDGE_TEMPERATURE = 0.2
JUDGE_TOP_K = 10
TestType = TestType.BENCHMARKING # Swap for desired test type

if __name__ == "__main__":


    #   +-------------------------------------------------------------------------------------+
    #   |                                                                                     |
    #   |  Example script to generate and evaluate responses for various tests.               |
    #   |  TestType is an enumeration that defines the type of test to be performed:          |
    #   |  - PROMPT_ALIGNMENT                                                                 |
    #   |  - SUMMARIZATION                                                                    |
    #   |  - HELPFULNESS                                                                      |
    #   |                                                                                     |
    #   |  Optional parameters generate_responses:                                            |
    #   |  n_responses can be set to specify the number of responses per prompt to generate.  |
    #   |                                                                                     |
    #   |  Optional parameters eval_responses:                                                |
    #   |  eval_archived=True can be set to evaluate all archived responses.                  |
    #   |  eval_range can be set to specify a range of responses to evaluate.                 |
    #   |                                                                                     |
    #   +-------------------------------------------------------------------------------------+

    #######################
    # Example usage of the script to generate and evaluate responses for different models.
    #######################

    NUM_RESPONSES = 3
    # EVAL_RANGE = (10, 100)

    MODELS = ["hermes3:70b-llama3.1-q8_0"]

    # generate_responses(test_type=TestType.PROMPT_ALIGNMENT, models=[MODEL], n_responses=NUM_RESPONSES)
    # generate_responses(test_type=TestType.HELPFULNESS, models=[MODEL], n_responses=NUM_RESPONSES)
    # generate_responses(test_type=TestType.SUMMARIZATION, models=MODELS, n_responses=NUM_RESPONSES)

    JUDGE1 = (JUDGE_MODEL1, JUDGE_SEED, JUDGE_TEMPERATURE, JUDGE_TOP_K)
    JUDGE2 = (JUDGE_MODEL2, JUDGE_SEED, JUDGE_TEMPERATURE, JUDGE_TOP_K)
    JUDGE3 = (JUDGE_MODEL3, JUDGE_SEED, JUDGE_TEMPERATURE, JUDGE_TOP_K)
    JUDGES = [JUDGE1, JUDGE3]

    if TestType == TestType.PROMPT_ALIGNMENT:
        generate_responses(test_type=TestType.PROMPT_ALIGNMENT, judges=JUDGES)
    if TestType == TestType.HELPFULNESS:
        generate_responses(test_type=TestType.HELPFULNESS, judges=JUDGES)
    if TestType == TestType.SUMMARIZATION:
        summaries = eval_responses(test_type=TestType.SUMMARIZATION, judges=JUDGES)

    # -- Run Benchmarking --
    if TestType == TestType.BENCHMARKING:
        asyncio.run(initBenchmarking(newExcel=False))