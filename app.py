import logging
import traceback
import os
from django.shortcuts import render

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.getenv('DATABASE_USERNAME', default='admin') + ':' + os.getenv('DATABASE_PASSWORD', default='password') + '@' + os.getenv('DATABASE_SERVER', default='localhost') + os.getenv('DATABASE_PORT', default='3306') + '/' + os.getenv('DATABASE_NAME')
app.secret_key = os.getenv('SECRET_KEY', default='8648d22e542ca1188d20de52b52c6d33d209704f508f21fc')

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

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

@app.route('/complete_task/<id>')
def complete_task(id):
    mentor = Task.query.get(id)
    mentor.complete =  True
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/incomplete_task/<id>')
def incomplete_task(id):
    mentor = Task.query.get(id)
    mentor.complete = False
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/add_task')
def add_task():
    task = Task(title=request.form.get('title'), description=request.form.get('description'), complete=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('tasks'))