from use_case_metrics import generate_responses, eval_responses
from utils import TestType
from llms import MODEL


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

    # NUM_RESPONSES = 1
    # EVAL_RANGE = (0, 10)

    # generate_responses(
    #     test_type=TestType.PROMPT_ALIGNMENT,
    #     model=MODEL,
    #     n_responses=NUM_RESPONSES,
    # )
    alignment = eval_responses(test_type=TestType.PROMPT_ALIGNMENT, eval_archived=True)
    
    # generate_responses(
    #     test_type=TestType.SUMMARIZATION,
    #     model=MODEL,
    #     n_responses=NUM_RESPONSES,
    # )
    summaries = eval_responses(test_type=TestType.SUMMARIZATION, eval_archived=True)
    
    # generate_responses(
    #     test_type=TestType.HELPFULNESS,
    #     model=MODEL,
    #     n_responses=NUM_RESPONSES,
    #     )
    helpfulness = eval_responses(test_type=TestType.HELPFULNESS, eval_archived=True)