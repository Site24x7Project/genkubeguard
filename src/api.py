from fastapi import FastAPI, UploadFile
from src import linter_runner, llm_handler, yaml_patcher, rag_memory

app = FastAPI()

@app.post("/analyze")
async def analyze_yaml(file: UploadFile):
    content = await file.read()
    issues = linter_runner.run_kube_linter(content)
    explanations = [llm_handler.explain(issue) for issue in issues]
    return {"issues": issues, "explanations": explanations}
