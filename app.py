from flask import Flask, jsonify, make_response, request, abort
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(Config)
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(64), index=True)
    status = db.Column(db.String(64), index=True)

    def as_dict(self):
        return {"title": self.title, "id": self.id, "description": self.description, "status": self.status}


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = [task.as_dict() for task in Task.query.all()]
    return jsonify(tasks)


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first_or_404()
    return jsonify(task.as_dict())


@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400, "Missing title")
    title = str(request.json['title'])
    description = str(request.json['description']) or None
    status = str(request.json['status']) or "Not Done"
    task = Task(title=title, description=description, status=status)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.as_dict())


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@cross_origin(methods=['OPTIONS', 'PUT'])
def update_task(task_id):
    if not request.json or not 'title' in request.json:
        abort(400, "Missing title")
    title = str(request.json['title'])
    task = Task.query.filter_by(id=task_id).first_or_404()
    description = str(request.json['description'] or task.description)
    status = str(request.json['status'] or task.status)
    task.title = title
    task.description = description
    task.status = status
    db.session.commit()
    return jsonify(task.as_dict())


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    else:
        abort(404, "Task not found")
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run()
