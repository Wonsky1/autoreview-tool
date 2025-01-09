from typing import List
from github.Repository import Repository
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from logging import getLogger
from core.config import settings
from prompts import review_single_file_prompt, review_single_file_summary_prompt

logger = getLogger(__name__)


def process_file(file_chunks: List[str], file_path: str, candidate_level: str) -> str:
    memory = ConversationBufferMemory()
    conversation_chain = ConversationChain(
        llm=settings.GENERATIVE_MODEL,
        memory=memory,
    )

    for i, chunk in enumerate(file_chunks):
        logger.info(f"Processing file: {file_path} - Chunk {i + 1}/{len(file_chunks)}")
        conversation_chain.invoke(
            {
                "input": review_single_file_prompt(
                    file_content=chunk,
                    file_path=file_path,
                    candidate_level=candidate_level,
                    chunk_num=i,
                    total_chunk_num=len(file_chunks),
                )
            }
        )

    file_summary = conversation_chain.invoke(
        {
            "input": review_single_file_summary_prompt(
                file_path=file_path, candidate_level=candidate_level
            )
        }
    )
    result = file_summary.get("response", f"Error processing file {file_path}")
    return result


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
