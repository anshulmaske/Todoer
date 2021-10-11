from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy, sqlalchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('homepage.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)