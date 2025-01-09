import unittest
from tools.texts import split_large_file, clear_github_url


class TestSplitLargeFile(unittest.TestCase):

    def test_split_large_file(self):
        file_content = "This is a test file.\nIt has multiple lines.\nEach line will be split."
        chunk_size = 50

        expected_result = [
            "This is a test file.\nIt has multiple lines.",
            "Each line will be split."
        ]

        result = split_large_file(file_content, chunk_size)

        self.assertEqual(result, expected_result)

    def test_split_large_file_single_chunk(self):
        file_content = "This is a short file."
        chunk_size = 100

        expected_result = ["This is a short file."]

        result = split_large_file(file_content, chunk_size)

        self.assertEqual(result, expected_result)

    def test_split_large_file_edge_case_empty(self):
        file_content = ""
        chunk_size = 50

        expected_result = []

        result = split_large_file(file_content, chunk_size)

        self.assertEqual(result, expected_result)


class TestClearGithubUrl(unittest.TestCase):
    def test_clear_github_url_valid(self):
        url = "https://github.com/username/repository"

        expected_result = "username/repository"

        result = clear_github_url(url)

        self.assertEqual(result, expected_result)

    def test_clear_github_url_invalid_domain(self):
        url = "https://otherdomain.com/username/repository"

        with self.assertRaises(ValueError):
            clear_github_url(url)

    def test_clear_github_url_missing_protocol(self):
        url = "github.com/username/repository"

        expected_result = "username/repository"

        result = clear_github_url(url)

        self.assertEqual(result, expected_result)

    def test_clear_github_url_invalid_url(self):
        url = "invalid-url"

        with self.assertRaises(ValueError):
            clear_github_url(url)
