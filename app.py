from logging import getLogger

from fastapi import FastAPI, HTTPException
from core.config import settings
from schemas.endpoints import RepositoryRequest
from tools.app_functions import send_files_to_model
from tools.texts import clear_github_url


logger = getLogger(__name__)

app = FastAPI()


@app.post("/review")
async def review_repository(request: RepositoryRequest):
    """
    Endpoint to review a GitHub repository.

    This endpoint receives a GitHub repository URL, along with information
    about the candidate's level and the assignment description, and generates
    a review based on the code present in the repository. The review is generated
    using an AI model that analyzes the repository files and provides feedback
    on code quality, areas of improvement, and overall performance.

    Args:
        request (RepositoryRequest): The request body containing the GitHub repository URL,
                                      the candidate's level (Junior, Middle, Senior), and the
                                      assignment description.

    Returns:
        dict: A dictionary containing the review result, including a summary of the
              repository analysis.

    Raises:
        HTTPException: If any error occurs during processing, a 500 HTTP exception is raised
                       with the error message.
    """
    try:
        repo_name = clear_github_url(str(request.github_repo_url))
        repo = settings.github_client.get_repo(repo_name)
        result = send_files_to_model(
            repo=repo,
            candidate_level=request.candidate_level,
            assignment_description=request.assignment_description,
        )
        return {"review": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
