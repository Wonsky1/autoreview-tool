import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app


class TestReviewRepository(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.settings.github_client")
    @patch("app.send_files_to_model")
    @patch("app.clear_github_url")
    def test_analyze_repository(self, mock_clear_github_url, mock_send_files_to_model, mock_github_client):
        mock_clear_github_url.return_value = "username/repository"

        mock_repo = MagicMock()
        mock_github_client.get_repo.return_value = mock_repo

        mock_send_files_to_model.return_value = "This is a review result"

        request_data = {
            "github_repo_url": "https://github.com/username/repository",
            "candidate_level": "Junior",
            "assignment_description": "Review repository files",
        }

        response = self.client.post("/review", json=request_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"review": "This is a review result"})

        mock_clear_github_url.assert_called_once_with("https://github.com/username/repository")
        mock_github_client.get_repo.assert_called_once_with("username/repository")
        mock_send_files_to_model.assert_called_once_with(
            repo=mock_repo,
            candidate_level="Junior",
            assignment_description="Review repository files",
        )

    @patch("app.settings.github_client")
    @patch("app.send_files_to_model")
    @patch("app.clear_github_url")
    def test_analyze_repository_error(self, mock_clear_github_url, mock_send_files_to_model, mock_github_client):
        mock_clear_github_url.return_value = "username/repository"

        mock_repo = MagicMock()
        mock_github_client.get_repo.return_value = mock_repo

        mock_send_files_to_model.side_effect = Exception("Error processing repository")

        request_data = {
            "github_repo_url": "https://github.com/username/repository",
            "candidate_level": "Junior",
            "assignment_description": "Review repository files",
        }

        response = self.client.post("/review", json=request_data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Error processing repository"})

        mock_clear_github_url.assert_called_once_with("https://github.com/username/repository")
        mock_github_client.get_repo.assert_called_once_with("username/repository")
        mock_send_files_to_model.assert_called_once_with(
            repo=mock_repo,
            candidate_level="Junior",
            assignment_description="Review repository files",
        )
