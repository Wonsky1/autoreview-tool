from typing import List
from github.Repository import Repository
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from logging import getLogger
from core.config import settings
from prompts import review_single_file_prompt, review_single_file_summary_prompt, review_one_chunk_file_prompt
from tools.redis_client import get_redis_client

logger = getLogger(__name__)


def process_file(
    file_chunks: List[str],
    file_path: str,
    candidate_level: str,
    assignment_description: str,
) -> str | None:
    """
    Processes a file in chunks and generates a review based on the file's content.

    This function takes in chunks of a file, processes each chunk sequentially,
    and generates a review or summary using a generative AI model. If the file
    is too large, it breaks it into smaller chunks and processes each chunk
    separately before generating a final summary.

    Args:
        file_chunks (List[str]): A list of file content chunks to be processed.
        file_path (str): The path of the file being reviewed.
        candidate_level (str): The candidate's level (Junior, Middle, Senior).
        assignment_description (str): The description of the coding assignment.

    Returns:
        str | None: The review or summary of the file if processing is successful,
                    otherwise returns `None` if no chunks are provided.
    """
    if not file_chunks:
        return None
    memory = ConversationBufferMemory()
    conversation_chain = ConversationChain(
        llm=settings.GENERATIVE_MODEL,
        memory=memory,
    )
    logger.info(f"Processing file: {file_path}")
    if len(file_chunks) > 1:
        for i, chunk in enumerate(file_chunks):
            logger.info(f"Chunk {i + 1}/{len(file_chunks)}")
            conversation_chain.invoke(
                {
                    "input": review_single_file_prompt(
                        file_content=chunk,
                        file_path=file_path,
                        candidate_level=candidate_level,
                        chunk_num=i,
                        total_chunk_num=len(file_chunks),
                        assignment_description=assignment_description,
                    )
                }
            )

        file_summary = conversation_chain.invoke(
            {
                "input": review_single_file_summary_prompt(
                    file_path=file_path,
                    candidate_level=candidate_level,
                    assignment_description=assignment_description,
                )
            }
        )
    else:
        file_summary = conversation_chain.invoke(
            {
                "input": review_one_chunk_file_prompt(
                    file_content=file_chunks[0],
                    file_path=file_path,
                    candidate_level=candidate_level,
                    assignment_description=assignment_description,
                )
            }
        )
    result = file_summary.get("response", f"Error processing file {file_path}")
    return result


def get_all_repository_paths(repo: Repository, path: str = "") -> List[str]:
    """
    Retrieves all file paths in a GitHub repository, starting from a specified path.

    This function retrieves the paths of all files within a GitHub repository,
    traversing the directory structure recursively. It supports caching the
    paths in Redis for faster retrieval on subsequent requests.

    Args:
        repo (Repository): The GitHub repository object.
        path (str, optional): The path within the repository to start from.
                               Defaults to an empty string, which corresponds to the root.

    Returns:
        List[str]: A list of all file paths in the repository.

    Raises:
        Exception: If there are issues retrieving the repository contents or processing the paths.
    """
    if settings.ENABLE_REDIS:
        redis_client = get_redis_client()
        cache_key = f"repo_paths:{repo.full_name}"

        cached_paths = redis_client.get(cache_key)
        if cached_paths:
            logger.info(f"Using cached paths for repository: {repo.full_name}")
            return eval(cached_paths)

    paths = []
    contents = repo.get_contents(path)
    for content in contents:
        if content.type == "dir":
            paths.extend(get_all_repository_paths(repo, content.path))
        else:
            paths.append(content.path)

    if settings.ENABLE_REDIS:
        redis_client.set(cache_key, str(paths), ex=settings.CACHE_EXPIRATION_MINUTES * 60)

    return paths
