from typing import List
from urllib.parse import urlparse


def split_large_file(file_content: str, chunk_size: int) -> List[str]:
    """
    Split a large file content into smaller chunks based on a specified chunk size.

    :param file_content: The content of the file as a single string.
    :param chunk_size: The maximum size (in characters) of each chunk. Defaults to 2048.
    :return: A list of file content chunks, where each chunk is a string of at most 'chunk_size' characters.
    """
    if not file_content:
        return []
    lines = file_content.split("\n")
    chunks = []
    current_chunk = []
    current_size = 0

    for line in lines:
        line_size = len(line)
        if current_size + line_size > chunk_size:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_size = 0
        current_chunk.append(line)
        current_size += line_size

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


def clear_github_url(url: str) -> str:
    """
    Extracts the repository path from a full GitHub URL.
    If the URL does not have a protocol, it assumes "https://" by default.

    Args:
        url (str): The full GitHub repository URL.

    Returns:
        str: The simplified repository path (username/repository).
    """
    try:
        # If the URL does not have a protocol, add "https://"
        if not url.startswith("http"):
            url = "https://" + url

        # Parse the URL
        parsed_url = urlparse(url)

        # Check if the netloc is github.com
        if parsed_url.netloc == "github.com":
            return parsed_url.path.lstrip("/")
        else:
            raise ValueError("The provided URL is not a valid GitHub repository URL.")
    except Exception as e:
        raise ValueError(f"Error processing the URL: {e}")
