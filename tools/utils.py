from typing import List
from github.Repository import Repository
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from logging import getLogger
from core.config import settings


logger = getLogger(__name__)


def process_file(file_chunks: List[str], file_path: str) -> str:
    memory = ConversationBufferMemory()
    conversation_chain = ConversationChain(
        llm=settings.GENERATIVE_MODEL,
        memory=memory,
    )

    for i, chunk in enumerate(file_chunks):
        logger.info(
            f"Processing file: {file_path} - Chunk {i + 1}/{len(file_chunks)}"
        )
        conversation_chain.invoke(
            {
                "input": f"This is a code snippet from {file_path}, Chunk {i + 1}/{len(file_chunks)}. Code: {chunk}"
            }
        )

    file_summary = conversation_chain.invoke(
        {
            "input": f"Finished analyzing all chunks for file: {file_path}. "
                     "Provide insights considering the prior context."
        }
    )
    return file_summary


def get_all_repository_paths(repo: Repository, path: str = "") -> List[str]:
    """
    Get all file paths in a GitHub repository.

    :param repo: The GitHub repository object.
    :param path: The path within the repository to start from (default is root).
    :return: A list of all file paths in the repository.
    """
    paths = []
    contents = repo.get_contents(path)

    for content in contents:
        if content.type == "dir":
            paths.extend(get_all_repository_paths(repo, content.path))
        else:
            paths.append(content.path)
    return paths
