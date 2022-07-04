from flask import Flask, jsonify, request

app = Flask(__name__)

from db.init import (
    create_new_task,
    delete_task_by_id,
    get_all_tasks_of_user,
    get_task_by_id,
    update_task_status,
)


@app.route("/")
def index():
    return "TODO Tasks API"


@app.route("/createtask", methods=["POST"])
def create_task():
    if request.method == "POST":
        task_info = request.get_json(cache=True)
        insert_result = create_new_task(
            title=task_info["title"],
            user_id=task_info["user_id"],
            description=task_info["description"],
            task_type=task_info["task_type"],
        )
        return jsonify(insert_result)
    else:
        return jsonify("Task created get")


@app.route("/task/<task_id>", methods=["GET"])
def get_task(task_id):
    task_row = get_task_by_id(task_id=task_id)
    return jsonify(task_row)


@app.route("/task/user/<user_id>")
def get_all_user_tasks(user_id):
    all_tasks = get_all_tasks_of_user(user_id=user_id)
    return jsonify(all_tasks)


@app.route("/task/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if request.method == "DELETE":
        delete_row = delete_task_by_id(task_id=task_id)
        return jsonify(delete_row)


@app.route("/task/update", methods=["POST"])
def update_task():
    task_info = request.get_json(cache=True)
    update_result = update_task_status(
        task_id=task_info["task_id"], new_status=task_info["new_task_type"]
    )
    return jsonify(update_result)


if __name__ == "__main__":
    app.run()
