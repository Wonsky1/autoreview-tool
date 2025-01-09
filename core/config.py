from logging import getLogger
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
from openai import OpenAI
from langchain_ollama import ChatOllama
from typing import Optional

logger = getLogger(__name__)


class Settings(BaseSettings):

    GITHUB_ACCESS_TOKEN: str
    LLM_API_CHAR_LIMIT: int = 2028
    OPENAI_MODEL_NAME: str = "gpt-4-turbo"
    LOCAL_DEVELOPMENT: bool = False
    OPENAI_API_KEY: Optional[str] = None
    
    client: Optional[OpenAI] = None  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @field_validator("client", mode="before")
    def validate_openai_client(cls, value: Optional[OpenAI], info: ValidationInfo):
        """
        Validates and initializes the OpenAI client if LOCAL_DEVELOPMENT is False.
        
        Args:
            value: The current value of the client field.
            info: Additional validation information, including other field values.
        
        Returns:
            The validated or initialized OpenAI client.
        
        Raises:
            ValueError: If OPENAI_API_KEY is missing when LOCAL_DEVELOPMENT is False.
        """
        if not info.data.get("LOCAL_DEVELOPMENT", False):
            if value is None:
                openai_api_key = info.data.get("OPENAI_API_KEY")
                if not openai_api_key:
                    raise ValueError("OPENAI_API_KEY must be provided when LOCAL_DEVELOPMENT is False.")
                value = OpenAI(api_key=openai_api_key)
        return value


settings = Settings()


def generate_response(system: str, human: str):
    """
    Generates a response based on the input text and the LOCAL_DEVELOPMENT setting.
    
    If LOCAL_DEVELOPMENT is True, uses the local Llama3 model. 
    If LOCAL_DEVELOPMENT is False, uses the OpenAI API.
    
    Args:
        system: The system message for the model.
        human: The input text for which the response is to be generated.
    
    Returns:
        A string containing the generated response from either the local model or the OpenAI API.
    """
    if settings.LOCAL_DEVELOPMENT:
        messages = [
            ("system", system),
            ("human", human)
        ]
        try:
            llm = ChatOllama(model="llama3")
            response = llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating response with Llama3: {e}")
            raise ValueError("Error generating response with Llama3.")
    
    else:
        if settings.client:
            try:
                chat_completion = settings.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": human}
                    ],
                    model=settings.OPENAI_MODEL_NAME
                )
                return chat_completion['choices'][0]['message']['content']
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {e}")
                raise ValueError("Error generating response with GPT-4.")
        else:
            logger.error(f"OpenAI client is not properly initialized.")
            raise ValueError("OpenAI client is not properly initialized.")
