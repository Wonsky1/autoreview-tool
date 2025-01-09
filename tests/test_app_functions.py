import unittest
from unittest.mock import patch, MagicMock

from tools.app_functions import send_files_to_model


class TestSendFilesToModel(unittest.TestCase):
    @patch("tools.app_functions.settings.GENERATIVE_MODEL.predict")
    @patch("tools.app_functions.settings")
    @patch("tools.app_functions.settings.GENERATIVE_MODEL")
    @patch("tools.app_functions.review_repository_files_prompt")
    @patch("tools.app_functions.process_file")
    @patch("tools.app_functions.split_large_file")
    @patch("github.Repository.Repository")
    @patch('tools.app_functions.get_all_repository_paths')
    def test_send_files_to_model(self, mock_get_all_repository_paths, mock_repository, mock_split_large_file,
                                 mock_process_file, mock_prompt, mock_GENERATIVE_MODEL, mock_settings, mock_predict):
        mock_get_all_repository_paths.return_value = ['path1', 'path2']
        mock_split_large_file.return_value = ['chunk1', 'chunk2']
        mock_process_file.return_value = 'summary'

        expected_result = "result"
        mock_predict.return_value = expected_result

        result = send_files_to_model(mock_repository, 'level', 'description')

        self.assertEqual(result, expected_result)

        mock_predict.assert_called_once()