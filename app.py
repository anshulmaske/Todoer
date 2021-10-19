from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, sqlalchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_test.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer , primary_key= True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    #testing
    todo_li = Todo.query.all()
    return render_template('homepage.html', todo_li=todo_li)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.("title")
    new_todo = Todo(title=title, comeplete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
