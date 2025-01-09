from typing import Literal
from pydantic import BaseModel, HttpUrl


class RepositoryRequest(BaseModel):
    """
    Schema for the /review POST endpoint request body.
    """

    assignment_description: str
    github_repo_url: HttpUrl
    candidate_level: Literal["Junior", "Middle", "Senior"]
