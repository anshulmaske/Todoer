from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from validator import emailValidator, nameValidator, passValidator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "temporary"
db = SQLAlchemy(app)
login_mgr = LoginManager()
login_mgr.init_app(app=app)
login_mgr.login_view = 'login'


@login_mgr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    priority = db.Column(db.String(1))
    date_added = db.Column(db.String(2))
    month_added = db.Column(db.String(3))
    date_due = db.Column(db.String(2))
    month_due = db.Column(db.String(3))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key =True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    username = db.Column(db.String(30), nullable = False, unique = True)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password_hash = db.Column(db.String(256))

    def setPass(self, password):
        self.password_hash = generate_password_hash(password=password, method="sha256")
    def checkPass(self, password):
        return check_password_hash(self.password_hash, password)



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
@login_required
def dashboard():
    todo_li = Todo.query.all()
    return render_template("homepage.html", todo_li=todo_li)

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    user = User()
    user.fname = request.form.get("fname")
    user.lname = request.form.get("lname")
    user.username = request.form.get("username")
    user.email = request.form.get("email")
    password = request.form.get("password")
    msg = {}
    data = {
        'fname': user.fname,
        'lname': user.lname,
        'username': user.username,
        'email': user.email,
    }
    flag = False
    if not emailValidator(user.email):
        msg["email"] = "Invalid email"
        flag = True
    if not passValidator(password):
        msg["pass"] = "Password requirements not met"
        flag = True
    if not nameValidator(user.username):
        msg["username"] = "Username requirements not met"
        flag = True

    if flag:
        return render_template("signup.html", msg = msg)

    user.setPass(password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for(".login"))

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    user = User.query.filter_by(username=request.form.get('username')).first()
    if user.checkPass(request.form.get('password')):
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html', msg = "Incorrect Credentials. Please Try Again")

@app.route('/logout', methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/add", methods=["POST","GET"])
def add():
    title = request.form.get("title")
    priority = request.form.get("priority")
    date_added = datetime.date.today()
    #TODO: Add due date and due month
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
    app.run(debug=True)
