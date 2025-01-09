from tools.texts import split_large_file
from tools.utils import get_all_repository_paths, process_file
from github.Repository import Repository
from logging import getLogger
from core.config import settings

logger = getLogger(__name__)


def send_files_to_model(repo: Repository) -> str:
    """
    Process all repository files and send them to the generative model for analysis.
    Clears conversation history for each file and provides an overall summary.
    """
    file_paths = get_all_repository_paths(repo)
    overall_verdicts = []

    for file_path in file_paths:
        file_content = repo.get_contents(file_path).decoded_content.decode()
        file_chunks = split_large_file(file_content, settings.LLM_API_CHAR_LIMIT)

        file_summary = process_file(file_chunks, file_path)
        overall_verdicts.append(f"File: {file_path}\n{file_summary}")

    overall_response = settings.GENERATIVE_MODEL.predict(
        f"Here is the analysis of all files:\n\n{''.join(overall_verdicts)}\n"
        "Summarize the overall analysis for the repository."
    )

    return overall_response
