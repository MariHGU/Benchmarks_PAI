from enum import IntEnum

class TestType(IntEnum):
    """
    Enum for different test types.
    """
    SUMMARIZATION = 1
    PROMPT_ALIGNMENT = 2
    HELPFULNESS = 3


if __name__ == "__main__":
    print(TestType.SUMMARIZATION)