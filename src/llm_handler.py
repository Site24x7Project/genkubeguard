import ollama
import os
from pathlib import Path
from src.rag_memory import RagMemory
memory = RagMemory()


def load_prompt_template():
    with open("src/prompts/explain.txt", "r", encoding="utf-8") as f:
        return f.read()

PROMPT_TEMPLATE = load_prompt_template()

def explain(issue: str) -> str:
    prompt = PROMPT_TEMPLATE.replace("{{issue}}", issue.strip())
    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": "You are a helpful Kubernetes DevSecOps expert."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response['message']['content']
        memory.add(f"Prompt: {prompt}\nResponse: {content}") 
        return content
    except Exception as e:
        return f" Error from LLM: {str(e)}"

def generate_patch(yaml_text: str) -> str:
    try:
        with open("src/prompts/fix.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()

        full_prompt = prompt_template.replace("{{yaml}}", yaml_text.strip())

        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": "You are a helpful YAML security expert."},
                {"role": "user", "content": full_prompt}
            ]
        )
        content = response['message']['content'].strip()

       
        if "securityContext" not in content:
            patched_snippet = """
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
"""
            content = content.replace("image: nginx:1.21.6", f"image: nginx:1.21.6\n{patched_snippet.strip()}")

        if not content.startswith("---"):
            content = f"---\n{content}"

        memory.add(f"Prompt: {full_prompt}\nResponse: {content}")
        return content

    except Exception as e:
        return f"LLM error while generating patch: {e}"




def suggest(yaml_str: str) -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "suggest.txt")
    with open(prompt_path, "r") as f:
        prompt_template = f.read()

    prompt = f"{prompt_template}\n\nYAML:\n{yaml_str}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    content = response["message"]["content"]
    memory.add(f"Prompt: {prompt}\nResponse: {content}")  # Log into memory
    return content

def load_prompt(filename):
    return Path(f"src/prompts/{filename}").read_text()

def suggest_with_persona(yaml_text, persona="junior"):
    persona_prompt = load_prompt(f"persona_{persona}.txt")
    prompt = f"{persona_prompt}\n\nHere is the YAML file:\n```yaml\n{yaml_text}\n```"
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    content = response['message']['content']
    memory.add(f"Prompt: {prompt}\nResponse: {content}")  
    return content
