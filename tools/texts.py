from typing import List


def split_large_file(file_content: str, chunk_size: int) -> List[str]:
    """
    Split a large file content into smaller chunks based on a specified chunk size.

    :param file_content: The content of the file as a single string.
    :param chunk_size: The maximum size (in characters) of each chunk. Defaults to 2048.
    :return: A list of file content chunks, where each chunk is a string of at most 'chunk_size' characters.
    """
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
