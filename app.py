from flask import Flask, session, request, Response, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
import os

import time
import sqlite3
import datetime

# Forms...
from forms import *


class Sql:

    def __init__(self):
        self.db = sqlite3.connect("./db.db")
        self.c = self.db.cursor()

    def query(self, query):
        return self.c.execute(query)

    def insert(self, *query):
        return self.c.execute(*query)

    def close(self):
        self.db.close()


app = Flask(__name__)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)



@app.route('/')
@app.route('/index', methods=["POST", "GET"])
def index():
    sql_instance = Sql()
    sql = "SELECT * FROM posts ORDER BY ID DESC"
    all_posts = sql_instance.query(sql).fetchall()
    sql_instance.close()

    return render_template("index.html", all_posts=all_posts)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = PwdForm(request.form)

    if request.method == "POST":
        print("LOGIN PRESSED")
        db = sqlite3.connect("./db.db")
        c = db.cursor()
        c.execute("SELECT * FROM users")
        usr = c.fetchall()

        username = form.username.data
        password = form.password.data

        for i in usr:  # Checks password and username against DB and redirects to index of successfull.
            if i[1] == username and i[3] == password:
                id = i[1]
                user = User(id)
                login_user(user)
                print("Authenticated... redirect please...")
                session["logged_in"] = True
                db.close()
                flash('You were successfully logged in...')
                return redirect(url_for("index"))

        flash('Invalid password provided')

    return render_template("login.html", form=form)


@app.route("/new_post", methods=["POST", "GET"])
@login_required
def new_post():
    form = PostForm(CombinedMultiDict((request.files, request.form)))

    if request.method == "POST":
        filename = None
        if form.post_image.has_file():
            image = form.post_image.data
            filename = secure_filename(image.filename)
            image.save(os.path.join('./upload/images', filename))
        title = form.title.data
        text = form.body.data
        date = datetime.datetime.now()
        author = current_user.get_id()

        post_db = sqlite3.connect("./db.db")
        c = post_db.cursor()
        try:
            c.execute("INSERT INTO posts(title,text,date,author,image) VALUES (?,?,?,?,?)",
                      (title, text, date, author, filename,))
            post_db.commit()
            post_db.close()
            print("INSERT OK")

            return redirect(url_for("index"))

        except Exception as error:
            flash(error)
            print(error)

    return render_template("new_post.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = UserRegistration(CombinedMultiDict((request.files, request.form)))
    if request.method == "POST":

        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        profile_pic = form.profile_pic.data
        print(profile_pic)
        print(type(profile_pic))
        email = form.email.data

        filename = None
        if form.profile_pic.has_file():
            print("has file...")
            image = form.profile_pic.data
            filename = secure_filename(image.filename)
            filename = username + filename
            image.save(os.path.join('./upload/images/profile_pic', filename))

        db = sqlite3.connect("./db.db")
        c = db.cursor()
        c.execute("INSERT INTO users(usr,pwd,first_name,last_name,profile_pic,email) VALUES (?,?,?,?,?,?)",
                  (username, password, first_name, last_name, filename, email,))
        db.commit()
        db.close()

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@login_required
@app.route("/leaderboard", methods=["POST", "GET"])
def leaderboard():
    db = sqlite3.connect("./db.db")
    c = db.cursor()
    c.execute("SELECT * FROM weight_bench ORDER BY weight DESC")
    result = c.fetchall()
    db.close()

    return render_template("leaderboard.html", result=result)


@login_required
@app.route("/my_weights", methods=["POST", "GET"])
def my_weights():
    form = RegisterWeights(request.form)
    form_delete = DeleteButton(request.form)

    user = current_user.get_id()
    db = sqlite3.connect("./db.db")
    c = db.cursor()
    c.execute("SELECT * FROM weight_bench WHERE usr=(?)", (user,))
    result_weights = c.fetchall()
    db.close()

    if request.method == "POST":
        print(request.form)

        if "submit" in request.form:
            time_date = form.time_date.data
            print(time_date)
            video = form.video.data
            weight = form.weight.data

            db = sqlite3.connect("./db.db")
            c = db.cursor()
            c.execute("INSERT INTO weight_bench(usr,weight,time_date,video) VALUES (?,?,?,?)",
                      (user, weight, time_date, video,))
            db.commit()
            db.close()

            return redirect(url_for("my_weights"))

        if "delete" in request.form:
            id_hidden = form_delete.id_hidden.data
            db = sqlite3.connect("./db.db")
            c = db.cursor()
            c.execute("DELETE from weight_bench WHERE ID=(?)", (id_hidden,))
            db.commit()
            db.close()

            return redirect(url_for("my_weights"))

    return render_template("my_weights.html", result_weights=result_weights, form=form, form_delete=form_delete)


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    session["logged_in"] = False
    logout_user()

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
