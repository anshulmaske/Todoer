import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    priority = db.Column(db.String(1))
    date_added = db.Column(db.String(2))
    month_added = db.Column(db.String(3))
    

@app.route('/')
def index():
    todo_li = Todo.query.all()
    return render_template("homepage.html", todo_li=todo_li)


@app.route("/add", methods=["POST","GET"])
def add():
    title = request.form.get("title")
    priority = request.form.get("priority")
    date_added = datetime.date.today()
    new_todo = Todo(title=title, complete=False, priority= priority, date_added = str(date_added.day).zfill(2), month_added = date_added.strftime('%B')[:3])
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run()
