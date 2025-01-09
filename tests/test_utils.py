import unittest
from unittest.mock import patch, MagicMock
from tools.utils import process_file, get_all_repository_paths


class TestProcessFile(unittest.TestCase):
    @patch("tools.utils.ConversationBufferMemory")
    @patch("tools.utils.ConversationChain")
    @patch("tools.utils.settings.GENERATIVE_MODEL")
    @patch("tools.utils.review_single_file_prompt")
    @patch("tools.utils.review_single_file_summary_prompt")
    def test_process_file(self, mock_review_single_file_summary_prompt, mock_review_single_file_prompt,
                          mock_generative_model, mock_conversation_chain, mock_conversation_buffer_memory):
        mock_conversation_chain.return_value = MagicMock()
        mock_conversation_chain_instance = MagicMock()
        mock_conversation_chain.return_value = mock_conversation_chain_instance
        mock_conversation_chain_instance.invoke.return_value = {"response": "File Summary"}

        mock_review_single_file_prompt.return_value = "File review prompt"
        mock_review_single_file_summary_prompt.return_value = "File summary prompt"

        file_chunks = ["This is chunk 1", "This is chunk 2"]
        file_path = "test/file/path"
        candidate_level = "Junior"
        assignment_description = "Code review for junior developer"

        result = process_file(file_chunks, file_path, candidate_level, assignment_description)

        self.assertEqual(result, "File Summary")
        mock_conversation_chain_instance.invoke.assert_called()

        mock_review_single_file_prompt.assert_any_call(
            file_content="This is chunk 1",
            file_path=file_path,
            candidate_level=candidate_level,
            chunk_num=0,
            total_chunk_num=2,
            assignment_description=assignment_description,
        )
        mock_review_single_file_prompt.assert_any_call(
            file_content="This is chunk 2",
            file_path=file_path,
            candidate_level=candidate_level,
            chunk_num=1,
            total_chunk_num=2,
            assignment_description=assignment_description,
        )
        mock_review_single_file_summary_prompt.assert_called_with(
            file_path=file_path,
            candidate_level=candidate_level,
            assignment_description=assignment_description,
        )
        mock_conversation_buffer_memory.assert_called_once()

    @patch("tools.utils.ConversationBufferMemory")
    @patch("tools.utils.ConversationChain")
    def test_process_file_empty_chunks(self, mock_conversation_chain, mock_conversation_buffer_memory):
        file_chunks = []
        file_path = "test/file/path"
        candidate_level = "Junior"
        assignment_description = "Code review for junior developer"

        result = process_file(file_chunks, file_path, candidate_level, assignment_description)

        self.assertIsNone(result)
        mock_conversation_chain.assert_not_called()
        mock_conversation_buffer_memory.assert_not_called()


class TestGetAllRepositoryPaths(unittest.TestCase):
    @patch("tools.utils.get_all_repository_paths")
    @patch("tools.utils.Repository")
    def test_get_all_repository_paths(self, mock_repository, mock_get_all_repository_paths):
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo

        mock_repo.get_contents.return_value = [
            MagicMock(type="file", path="file1.py"),
            MagicMock(type="dir", path="dir1"),
            MagicMock(type="file", path="dir1/file2.py"),
        ]

        repo = mock_repo
        path = ""

        result = get_all_repository_paths(repo, path)

        self.assertEqual(result, ["file1.py", "dir1/file2.py"])

        mock_repo.get_contents.assert_called_with(path)
        mock_get_all_repository_paths.assert_called_with(repo, "dir1")

    @patch("tools.utils.Repository")
    def test_get_all_repository_paths_empty_repo(self, mock_repository):
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo

        mock_repo.get_contents.return_value = []

        repo = mock_repo
        path = ""

        result = get_all_repository_paths(repo, path)

        self.assertEqual(result, [])

        mock_repo.get_contents.assert_called_with(path)


if __name__ == "__main__":
    unittest.main()
