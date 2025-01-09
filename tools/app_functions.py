from prompts import review_repository_files_prompt
from tools.texts import split_large_file
from tools.utils import get_all_repository_paths, process_file
from github.Repository import Repository
from logging import getLogger
from core.config import settings

logger = getLogger(__name__)


def send_files_to_model(
    repo: Repository, candidate_level: str, assignment_description: str
) -> str:
    """
    Process all repository files and send them to the generative model for analysis.
    Clears conversation history for each file and provides an overall summary.
    """
    file_paths = get_all_repository_paths(repo)
    verdicts = []

    for file_path in file_paths:
        file_content = repo.get_contents(file_path).decoded_content.decode()
        file_chunks = split_large_file(file_content, settings.LLM_API_CHAR_LIMIT)

        file_summary = process_file(
            file_chunks, file_path, candidate_level, assignment_description
        )
        if not file_summary:
            continue
        verdicts.append(f"File: {file_path}\n{file_summary}")
    if not verdicts:
        raise Exception("There was an error processing the repository files.")
    prompt = review_repository_files_prompt(
        file_summaries="".join(verdicts),
        candidate_level=candidate_level,
        assignment_description=assignment_description,
    )
    overall_response = settings.GENERATIVE_MODEL.predict(prompt)

    return overall_response
