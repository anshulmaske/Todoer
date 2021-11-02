from datetime import time
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, sqlalchemy

import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_test.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    priority = db.Column(db.String(1))


@app.route('/')
def index():
    # testing
    todo_li = Todo.query.all()
    return render_template("homepage.html", todo_li=todo_li)


@app.route("/add", methods=["POST","GET"])
def add():
    print("here")
    title = request.form.get("title")
    priority = request.form.get("priority")
    print(title, priority)
    new_todo = Todo(title=title, complete=False, priority= priority)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    #testing
    # c = [True, False]
    # p = ['L', 'M', 'H']
    # d = ['plate', 'bowl', 'toilet', 'socks', 'vase', 'table', 'zipper', 'eraser', 'soda can', 'headphones', 'cat', 'pen', 'bag', 'playing card', 'cookie jar', 'pants', 'truck', 'teddies', 'face wash', 'conditioner']
    # for x in range(20):
    #     t = Todo(title = random.choice(['buy ','sell '])+random.choice(d), complete = random.choice(c), priority = random.choice(p))
    #     db.session.add(t)
    # db.session.commit()
    app.run(debug=True)
