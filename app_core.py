from flask import Flask, Response, jsonify


app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Setup CI/CD", "status": "done"},
    {"id": 2, "title": "Write Unit Tests", "status": "in_progress"},
    {"id": 3, "title": "Complete Documentation", "status": "pending"},
]


def get_task_statistics(task_list):
    done = 0
    in_progress = 0
    pending = 0

    for task in task_list:
        if task["status"] == "done":
            done += 1
        elif task["status"] == "in_progress":
            in_progress += 1
        elif task["status"] == "pending":
            pending += 1

    return {
        "total": len(task_list),
        "done": done,
        "in_progress": in_progress,
        "pending": pending,
    }


@app.get("/")
def home():
    return Response("DevOps Midterm API is running!", mimetype="text/plain")


@app.get("/api/health")
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"})


@app.get("/api/tasks")
def get_tasks():
    return jsonify(tasks)


@app.get("/api/stats")
def get_stats():
    return jsonify(get_task_statistics(tasks))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)