import strawberry
from typing import List
from src.llm_handler import explain, generate_patch, suggest, suggest_with_persona
from src import linter_runner

@strawberry.type
class AnalysisResult:
    issues: List[str]
    explanations: List[str]

@strawberry.type
class PatchResult:
    patched_yaml: str

@strawberry.type
class SuggestionResult:
    suggestions: str

@strawberry.type
class Query:
    @strawberry.field
    def analyze(self, yaml_str: str) -> AnalysisResult:
        issues = linter_runner.run_kube_linter(yaml_str.encode("utf-8"))
        explanations = [explain(issue) for issue in issues]
        return AnalysisResult(issues=issues, explanations=explanations)

    @strawberry.field
    def health(self) -> str:
        return "GraphQL API is up and running"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def patch(self, yaml_str: str) -> PatchResult:
        return PatchResult(patched_yaml=generate_patch(yaml_str))
    
    @strawberry.mutation
    def suggest(self, yaml_str: str) -> SuggestionResult:
        return SuggestionResult(suggestions=suggest(yaml_str))
    
    @strawberry.mutation
    def suggest_with_persona(self, yaml_str: str, persona: str) -> SuggestionResult:
        return SuggestionResult(suggestions=suggest_with_persona(yaml_str, persona))

schema = strawberry.Schema(query=Query, mutation=Mutation)
