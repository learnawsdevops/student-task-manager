from flask import Flask, jsonify, request
from mysql.connector import Error

import database
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.errorhandler(Error)
    def database_error(error):
        app.logger.error("Database error: %s", error)
        return jsonify({"error": "Database unavailable"}), 503

    @app.get("/api/health")
    def health():
        if database.database_health():
            return jsonify({"status": "ok", "database": "connected"}), 200
        return jsonify({"status": "degraded", "database": "unavailable"}), 503

    @app.get("/api/tasks")
    def get_tasks():
        return jsonify(database.fetch_tasks()), 200

    @app.post("/api/tasks")
    def add_task():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "JSON body is required"}), 400

        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Task title is required"}), 400

        title = title.strip()
        if len(title) > 255:
            return jsonify({"error": "Task title must be 255 characters or fewer"}), 400

        return jsonify(database.create_task(title)), 201

    @app.patch("/api/tasks/<int:task_id>")
    def update_task(task_id):
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("completed"), bool):
            return jsonify({"error": "completed must be true or false"}), 400

        task = database.update_task(task_id, data["completed"])
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task), 200

    @app.delete("/api/tasks/<int:task_id>")
    def remove_task(task_id):
        if not database.delete_task(task_id):
            return jsonify({"error": "Task not found"}), 404
        return "", 204

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
