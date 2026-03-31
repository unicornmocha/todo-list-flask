from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    checked = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task_name = request.form.get('task')
        if task_name:
            new_task = Todo(name=task_name)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('home'))
    
    todos = db.session.scalars(select(Todo).order_by(Todo.checked, Todo.id)).all()
    return render_template('index.html', items=todos)

@app.route('/checked/<int:task_id>', methods=['POST'])
def toggle_checked(task_id):
    task = db.session.get(Todo, task_id)
    if task:
        task.checked = not task.checked
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = db.session.get(Todo, task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)