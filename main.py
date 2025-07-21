from use_case_metrics import generate_responses, eval_responses
from utils import TestType
from llms import JudgeParams

MODEL = "dolphin3:8b-llama3.1-fp16"
JUDGE_MODEL1 = "nhn-large:latest" # "deepseek-r1:32b-qwen-distill-fp16" # OLLAMA
JUDGE_MODEL2 = "nhn-medium:latest" # "devstral:24b-small-2505-fp16" # OLLAMA 
JUDGE_MODEL3 = "hermes3:70b-llama3.1-fp16" # OLLAMA
JUDGE_SEED = 42
JUDGE_TEMPERATURE = 0.2
JUDGE_TOP_K = 10

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
    

    # generate_responses(test_type=TestType.PROMPT_ALIGNMENT, model=MODEL, n_responses=NUM_RESPONSES)
    # generate_responses(test_type=TestType.HELPFULNESS, model=MODEL, n_responses=NUM_RESPONSES)
    # generate_responses(test_type=TestType.SUMMARIZATION, model=MODEL, n_responses=NUM_RESPONSES)
    
    JUDGE1 = JudgeParams(model_name=JUDGE_MODEL1, seed=JUDGE_SEED, temperature=JUDGE_TEMPERATURE, top_k=JUDGE_TOP_K)
    JUDGE2 = JudgeParams(model_name=JUDGE_MODEL2, seed=JUDGE_SEED, temperature=JUDGE_TEMPERATURE, top_k=JUDGE_TOP_K)
    JUDGE3 = JudgeParams(model_name=JUDGE_MODEL3, seed=JUDGE_SEED, temperature=JUDGE_TEMPERATURE, top_k=JUDGE_TOP_K)
    JUDGES = [JUDGE1, JUDGE2, JUDGE3]

    alignment = eval_responses(test_type=TestType.PROMPT_ALIGNMENT, judges=JUDGES)
    helpfulness = eval_responses(test_type=TestType.HELPFULNESS, judges=JUDGES)
    # summaries = eval_responses(test_type=TestType.SUMMARIZATION, judges=JUDGES)

