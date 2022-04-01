import logging
import traceback
import os

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hapydcojjcnwde:7f512ce444bfda3588d81261a25b4299705f6f81cad27803b07d3a13c0a900b5@ec2-52-3-60-53.compute-1.amazonaws.com:5432/d1t0317bcb2r1e'
app.secret_key = os.getenv('SECRET_KEY', default='8648d22e542ca1188d20de52b52c6d33d209704f508f21fc')

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run()

@app.route('/', methods=['GET'])
def admin():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/tasks', methods=['GET'])
def tasks():
    tasks = Task.query.all()
    return render_template('checklist.html', tasks=tasks)

@app.route('/complete_task/<id>', methods=['GET'])
def complete_task(id):
    mentor = Task.query.get(id)
    mentor.complete =  True
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/incomplete_task/<id>', methods=['GET'])
def incomplete_task(id):
    mentor = Task.query.get(id)
    mentor.complete = False
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/add_task', methods=['POST'])
def add_task():
    task = Task(title=request.form.get('title'), description=request.form.get('description'), complete=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/delete_task/<id>', methods=['GET'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))