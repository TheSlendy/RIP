from flask import Flask, jsonify, make_response, request, abort
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(64), index=True)
    status = db.Column(db.Boolean(), index=True)

    def __repr__(self):
        return '<Title: {}, Id: {}, Description: {}, Status: {}>'.format(self.title, self.id, self.description,
                                                                         self.status)


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = str(Task.query.all())
    return jsonify(tasks)


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = str(Task.query.filter_by(id=task_id).first_or_404())
    return jsonify(task)


@app.route('/api/tasks', methods=['POST'])
def create_task():  # JSON file example: {"title": "Name", "description": "Something", "status": false}
    if not request.json or not 'title' in request.json:
        abort(400, "Missing title")
    title = str(request.json['title'])
    if Task.query.filter_by(title=title):
        abort(400, "Task with this title has already exist")
    description = str(request.json['description'] or None)
    status = bool(request.json['status'] or False)
    task = Task(title=title, description=description, status=status)
    db.session.add(task)
    db.session.commit()
    return jsonify(str(task))


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
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
    return jsonify(str(task))


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
