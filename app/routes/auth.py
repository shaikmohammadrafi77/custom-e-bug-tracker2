# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db, login_manager

# Blueprint definition
auth_bp = Blueprint("auth", __name__)

# -------------------------
# Login route
# -------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard.index"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

# -------------------------
# Registration route
# -------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("User with this username or email already exists.", "danger")
            return redirect(url_for("auth.register"))

        # Create new user
        new_user = User(
            name=name,
            username=username,
            email=email,
            role="User"
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# -------------------------
# Logout route
# -------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))

# -------------------------
# User loader for Flask-Login
# -------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

