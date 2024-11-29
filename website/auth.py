from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if user with this email exists or not
        user = User.query.filter_by(email=email).first()
        if user:
            # check is password is correct
            if check_password_hash(user.password, password):
                # login successfull
                flash("Logged in Successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("User with this email does not exists!", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return "<h1>Logout</h1>"

@auth.route("/signup",  methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #basic input validations
        if len(email) < 1:
            flash("Email must not be empty", category="error")
        elif len(firstName) < 1:
            flash("firstName must not be empty", category="error")
        elif len(password1) < 1:
            flash("Password must not be empty", category="error")
        elif len(password2) < 1:
            flash("Confirm Password must not be empty", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        else:

            #check if user with this email already exists
            user = User.query.filter_by(email=email)
            if user:
                flash("User with this email already exists!", category="error")
            else: 

                # pass the data to db
                # create new user
                new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method="sha256"))
                db.session.add(new_user)
                db.session.commit()

                login_user(user, remember=True)
                flash("Account created", category="success")

                return redirect(url_for("views.home"))
                # same as return redirect("/") but it is better to use above one


    return render_template("signup.html", user=current_user)