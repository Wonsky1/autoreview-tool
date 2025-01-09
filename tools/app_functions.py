import os

from tools.texts import split_large_file
from tools.utils import get_all_repository_paths
from github.Repository import Repository
from logging import getLogger
from core.config import settings
from core.config import generate_response

logger = getLogger(__name__)


def send_files_to_openai(repo: Repository) -> str:
    """Process all repository files and send them to OpenAI for analysis."""
    file_paths = get_all_repository_paths(repo)

    overall_verdicts = []
    for file_path in file_paths:
        file_content = repo.get_contents(file_path).decoded_content.decode()
        file_chunks = split_large_file(file_content, settings.LLM_API_CHAR_LIMIT)
        chunk_analysis_results = []

        for i, chunk in enumerate(file_chunks):
            logger.info(
                f"Processing file: {file_path} - Chunk {i + 1}/{len(file_chunks)}"
            )
            response = generate_response(
                system="Describe this code",
                human=f"This is a code snippet from {file_path}, Chunk {i + 1}/{len(file_chunks)}. Code: {chunk} ",
            )
            chunk_analysis_results.append(response)

        formatted_chunk_analysis = "\n".join(
            [f"verdict {i + 1}:\n{chunk}" for i, chunk in enumerate(chunk_analysis_results)])
        # make sure to provide file path, maybe use dict for metadata saving
        overall_response = generate_response(
            system="Here is your previously reported info about the code, summarize this app and return an overall verdict for the file",
            human=f"previous verdicts: {formatted_chunk_analysis}",
        )
        overall_verdicts.append(overall_response)

    formatted_overall_verdicts = "\n".join(overall_verdicts)

    result = generate_response(
        system="Here is your overall verdicts for each of the file, summarize this app and return an overall verdict",
        human=formatted_overall_verdicts,
    )

    return result
