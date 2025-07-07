from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
import yaml
import asyncio

from src import linter_runner, llm_handler
from src.schema import Query as GQLQuery, Mutation as GQLMutation

app = FastAPI()

# Enable CORS for Swagger UI and other origins if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Analyze Endpoint 
@app.post("/analyze")
async def analyze_yaml(file: UploadFile = File(...)):
    content = await file.read()
    issues = linter_runner.run_kube_linter(content)

    
    if len(issues) == 1 and issues[0].strip().lower() == "no lint issues found.":

        return {
            "issues": issues,
            "explanations": [" No issues, so no explanations needed."]
        }

    # Run LLM explanations in parallel
    loop = asyncio.get_event_loop()

    async def run_explain(issue):
        return await loop.run_in_executor(None, llm_handler.explain, issue)

    explanations = await asyncio.gather(*(run_explain(issue) for issue in issues))

    return {"issues": issues, "explanations": explanations}


@app.post("/patch")
async def patch_yaml(file: UploadFile = File(...)):
    raw = (await file.read()).decode("utf-8")
    docs = list(yaml.safe_load_all(raw))

    has_deployment = any(doc.get("kind") == "Deployment" for doc in docs)
    if not has_deployment:
        return {"patched_yaml": raw}

    patched = llm_handler.generate_patch(raw)
    return {"patched_yaml": patched}


@app.post("/suggest")
async def suggest_improvements(file: UploadFile = File(...)):
    yaml_str = (await file.read()).decode("utf-8")
    suggestions = llm_handler.suggest(yaml_str)
    return {"suggestions": suggestions}

@app.post("/suggest-persona")
async def suggest_for_persona(
    file: UploadFile = File(...),
    persona: str = Query("junior")
):
    yaml_str = (await file.read()).decode("utf-8")
    persona_suggestions = llm_handler.suggest_with_persona(yaml_str, persona)
    return {"persona_suggestions": persona_suggestions}


@app.get("/memory")
def get_recent_memories(q: str = Query(..., description="Query term for RAG memory")):
    results = llm_handler.memory.search(q)
    return {"related": results}


schema = strawberry.Schema(query=GQLQuery, mutation=GQLMutation)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
