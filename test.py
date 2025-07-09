from use_case_metrics import generate_responses, eval_responses
from utils import TestType
import utils
import hashlib, time


if __name__ == "__main__":
    generate_responses(
        test_type=TestType.SUMMARIZATION,
        model="nhn-small:latest"
    )
    generate_responses(
        test_type=TestType.PROMPT_ALIGNMENT,
        model="nhn-small:latest"
    )
    generate_responses(
        test_type=TestType.HELPFULNESS,
        model="nhn-small:latest"
    )


    summaries = eval_responses(test_type=TestType.SUMMARIZATION)
    alignment = eval_responses(test_type=TestType.PROMPT_ALIGNMENT)
    helpfulness = eval_responses(test_type=TestType.HELPFULNESS)



# def test_summarization(
#     model: str= MODEL, 
#     api_key_file: str = ".api_key.txt",
#     prompts_file: str = "prompts/summarization_prompts.txt",
#     write_results: bool = True,
#     result_file: str = "results.xlsx",
#     ) -> List[tuple]:

#     """    Test the summarization model with a given prompt.

#     Args:
#         model (str): The model to use for summarization.
#         prompts_file (str): The file containing prompts for summarization.

#     Returns:
#         tuple: A tuple containing the score and reason from the metric evaluation.
#     """
#     Logger = utils.CustomLogger()
#     Logger.info("Init eval model")

#     # JudgeLLM = GroqModel()
#     JudgeLLM = OllamaLocalModel(
#         model=JUDGE_MODEL,
#         base_url=BASE_URL,
#         api_key_file=".api_key.txt",
#         seed=JUDGE_SEED,
#         temperature=JUDGE_TEMPERATURE
#     )

#     Logger.info("Init model")

#     LLM = OllamaLocalModel(
#         model=model,
#         base_url=BASE_URL,
#         api_key_file=api_key_file
#     )

#     Logger.info("Successful")
#     Logger.info("Loading prompts from file...")

#     with open(prompts_file, "r") as f:
#         prompts = [line.strip() for line in f if line.strip()]

#     summarization_scores = []

#     for i, prompt in enumerate(prompts):
#         Logger.info("Generating response for %d. prompt", i + 1)
#         response = LLM.generate(prompt)

#         # actual_output = client.chat(
#         #     model="gemma3n:e4b-it-q8_0",
#         #     messages=[
#         #         {
#         #             "role": "user",
#         #             "content": input,
#         #         }
#         #     ],
#         #     stream=False,
#         # ).message.content

#         Logger.info("Creating test case")

#         test_case = LLMTestCase(
#             input=prompt,
#             actual_output=response,
#         )

#         Logger.info("Preparing metric")

#         summarization_metric = SummarizationMetric(
#             threshold=0.5,
#             model=JudgeLLM
#         )

#         Logger.info("Measuring...")

#         summarization_score = summarization_metric.measure(test_case)
#         Logger.info("Measurement complete. Score: %s", summarization_score)

#         if write_results:
#             Logger.info("Writing result to file...")

#             utils.save_eval_results_to_xlsx(
#                 type_of_test="Summarization",
#                 model_name=model,
#                 results=[(summarization_score, summarization_metric.reason)],
#                 file_name=result_file,
#                 prompt_id=i,
#                 judge_params=(JudgeLLM.get_model_name(), JudgeLLM.get_seed(), JudgeLLM.get_temperature()),
#             )

#         summarization_scores.append((summarization_score, summarization_metric.reason))

#     return summarization_scores
