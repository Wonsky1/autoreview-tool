import logging
from logging import getLogger

from github import Github, Auth
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from typing import Optional

logger = getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    CACHE_EXPIRATION_MINUTES: int = 60

    GITHUB_ACCESS_TOKEN: str
    LLM_API_CHAR_LIMIT: int = 2028
    OPENAI_MODEL_NAME: str = "gpt-4-turbo"
    LOCAL_DEVELOPMENT: bool = False
    OPENAI_API_KEY: Optional[str] = None
    GENERATIVE_MODEL: Optional[ChatOllama | ChatOpenAI] = None

    github_client: Optional[Github] = None

    @field_validator("GENERATIVE_MODEL")
    def validate_generative_model(
        cls, value: Optional[ChatOpenAI | ChatOllama], info: ValidationInfo
    ):
        """
        Validates and initializes the appropriate generative model based on LOCAL_DEVELOPMENT.

        Args:
            value: The current value of the GENERATIVE_MODEL field.
            info: Validation information containing other field values.

        Returns:
            The appropriate generative model (ChatOpenAI or ChatOllama).

        Raises:
            ValueError: If OPENAI_API_KEY is missing when LOCAL_DEVELOPMENT is False.
        """
        if info.data.get("LOCAL_DEVELOPMENT", False):
            logger.info("Using local development model: Llama3")
            return ChatOllama(model="llama3")

        openai_api_key = info.data.get("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY must be provided when LOCAL_DEVELOPMENT is False."
            )

        logger.info("Using remote model: OpenAI GPT")
        return ChatOpenAI(
            model=info.data.get("OPENAI_MODEL_NAME", "gpt-4-turbo"),
            openai_api_key=openai_api_key,
        )

    @field_validator("github_client", mode="before")
    def validate_github_client(cls, value: Optional[Github], info: ValidationInfo):
        """
        Validates and initializes the GitHub client.

        Args:
            value: The current value of the github_client field.
            info: Validation information containing other field values.

        Returns:
            The initialized GitHub client.

        Raises:
            ValueError: If GITHUB_ACCESS_TOKEN is missing.
        """
        github_access_token = info.data.get("GITHUB_ACCESS_TOKEN")
        if not github_access_token:
            raise ValueError("GITHUB_ACCESS_TOKEN must be provided.")

        logger.info("Initializing GitHub client...")
        auth = Auth.Token(github_access_token)
        return Github(auth=auth)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
