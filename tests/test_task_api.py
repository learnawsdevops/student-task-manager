import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "application", "backend"))

from app import create_app


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    @patch("database.database_health", return_value=True)
    def test_health(self, health):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["database"], "connected")

    @patch("database.fetch_tasks", return_value=[
        {"id": 1, "title": "Study", "completed": False, "created_at": "2026-01-01"}
    ])
    def test_get_tasks(self, fetch):
        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["title"], "Study")

    @patch("database.create_task", return_value={
        "id": 1, "title": "Study", "completed": False, "created_at": "2026-01-01"
    })
    def test_create_task(self, create):
        response = self.client.post("/api/tasks", json={"title": " Study "})
        self.assertEqual(response.status_code, 201)
        create.assert_called_once_with("Study")

    def test_create_task_rejects_empty_title(self):
        response = self.client.post("/api/tasks", json={"title": "  "})
        self.assertEqual(response.status_code, 400)

    @patch("database.update_task", return_value={
        "id": 1, "title": "Study", "completed": True, "created_at": "2026-01-01"
    })
    def test_complete_task(self, update):
        response = self.client.patch("/api/tasks/1", json={"completed": True})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["completed"])

    @patch("database.delete_task", return_value=True)
    def test_delete_task(self, delete):
        response = self.client.delete("/api/tasks/1")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
