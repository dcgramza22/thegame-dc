import logging
import traceback
import os

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', default='8648d22e542ca1188d20de52b52c6d33d209704f508f21fc')

if __name__ == '__main__':
    app.run()

@app.route('/', methods=['GET'])
def admin():
    if request.method == 'GET':
        return render_template('home.html')