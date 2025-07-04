from summarizing import test_summarization
from helpfulness import test_helpfulness
from prompt_alignment import test_prompt_alignment
from utils import MODEL, JUDGE_MODEL, JUDGE_SEED, JUDGE_TEMPERATURE


if __name__ == "__main__":
    # Example usage for summarization
    model = MODEL
    prompts_file = "prompts/summarization_prompts.txt"
    
    summarization_results = test_summarization(model=model, prompts_file=prompts_file, write_results=True)
    
    # Example usage for helpfulness
    helpfulness_results = test_helpfulness(model=model, prompts_file=prompts_file, write_results=True)
    
    # Example usage for prompt alignment
    prompt_alignment_results = test_prompt_alignment(model=model, prompts_file=prompts_file, write_results=True)
    
    print("Summarization Results:", summarization_results)
    print("Helpfulness Results:", helpfulness_results)
    print("Prompt Alignment Results:", prompt_alignment_results)