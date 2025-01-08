from typing import List


def split_string_by_length(s: str, length: int) -> List[str]:
    """
    Split a string into chunks of a specified length.

    :param s: The input string to be split.
    :param length: The maximum length of each chunk.
    :return: A list of string chunks, each with a maximum length of 'length'.
    """
    return [s[i:i + length] for i in range(0, len(s), length)]
