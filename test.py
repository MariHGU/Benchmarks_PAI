from utils import OllamaLocalModel, CustomLogger

logger = CustomLogger()


logger.info("initialzing evaluation model...")

model = OllamaLocalModel(
    model="gemma3n:e4b-it-q8_0",
    base_url="https://beta.chat.nhn.no/ollama",
    api_key_file=".api_key.txt"
)

logger.info("Model initialized successfully.")

input_text = "Hello there"

logger.info("Generating response for input: %s", input_text)
actual_output = model.generate(input_text)
logger.info("Response generated successfully.")

print("Input:", input_text)
print("Output:", actual_output)
