from flask import Flask,render_template
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
    print(todo_li)
    return render_template('homepage.html')

if __name__ == '__main__':
    db.create_all()
    new_todo = Todo(title='1st todo', complete = False)
    db.session.add(new_todo)
    db.session.commit()
    app.run(debug=True)