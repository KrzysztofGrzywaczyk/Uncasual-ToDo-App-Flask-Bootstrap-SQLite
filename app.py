"""
Web ToDo-type aplication, where user is able to:
- Add a new task
- Mark task as completed and reverse this process.
- Archive Completed tasks to another section and restores them
- Delete tasks completely

Created using flask micro-freamwork and SQLAlchemy to connect to SQLite database
and also Bootstrap for stylistic purposes.
"""


from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db=SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200), default=None)
    complete = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)


with app.app_context():
    db.create_all()


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    new_task = Task(name = name)
    db.session.add(new_task)
    db.session.commit()

    if request.method == 'POST':
        name = request.form.get("name")
        flash(f'Succesfully created task: {name}', 'success')

    return redirect(url_for('index'))


@app.route('/archive/<id>')
def archive(id):
    task = Task.query.filter_by(id=id).first()
    task.active = not task.active
    db.session.commit()
    if task.active:
        flash(f'Succesfully restored: {task.name}', 'secondary')
    else:
        flash(f'Succesfully archived: {task.name}', 'secondary')
    return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete(id : bool):
    task = Task.query.filter_by(id=id).first()
    if task:
        name = task.name
        flash(f'Succesfully deleted task: {name}', 'warning')
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id : bool):
    task = Task.query.filter_by(id=id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/')
def index():
    all_tasks = Task.query.all()
    sum_of_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(complete=True).count()
    uncompleted_tasks = Task.query.filter_by(complete=False).count()
    return render_template('dashboard/index.html', **locals())


@app.route('/about')
def about():
    return render_template('dashboard/about.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'

    app.run(debug=True)