from logging import getLogger
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
from langchain_community.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
from typing import Optional, Union

logger = getLogger(__name__)


class Settings(BaseSettings):

    GITHUB_ACCESS_TOKEN: str
    LLM_API_CHAR_LIMIT: int = 2028
    OPENAI_MODEL_NAME: str = "gpt-4-turbo"
    LOCAL_DEVELOPMENT: bool = False
    OPENAI_API_KEY: Optional[str] = None
    GENERATIVE_MODEL: Optional[ChatOllama | ChatOpenAI] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @field_validator("GENERATIVE_MODEL", mode="before")
    def validate_generative_model(cls, value: Optional[ChatOpenAI | ChatOllama], info: ValidationInfo):
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
            raise ValueError("OPENAI_API_KEY must be provided when LOCAL_DEVELOPMENT is False.")

        logger.info("Using remote model: OpenAI GPT")
        return ChatOpenAI(model=info.data.get("OPENAI_MODEL_NAME", "gpt-4-turbo"), openai_api_key=openai_api_key)


settings = Settings()
