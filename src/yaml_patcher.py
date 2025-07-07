from src import llm_handler

def generate_patch(yaml_str: str) -> str:
    """
    Delegates to the LLM handler to generate a patch for the given YAML input.
    """
    return llm_handler.generate_patch(yaml_str)
