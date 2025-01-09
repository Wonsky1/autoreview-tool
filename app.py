from fastapi import FastAPI, HTTPException
from core.config import settings
from schemas.endpoints import RepositoryRequest
from tools.app_functions import send_files_to_model
from tools.texts import clear_github_url

app = FastAPI()


@app.post("/review")
async def analyze_repository(request: RepositoryRequest):
    try:
        repo_name = clear_github_url(str(request.github_repo_url))
        print(settings.GENERATIVE_MODEL)
        repo = settings.github_client.get_repo(repo_name)
        result = send_files_to_model(repo, request.candidate_level)
        return {"review": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
