# app/routes/project.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Project   # absolute import
from app import db               # absolute import

# Blueprint definition
project_bp = Blueprint("project", __name__)

# -------------------------
# List and create projects
# -------------------------
@project_bp.route("/", methods=["GET", "POST"])
@login_required
def list_projects():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        # Create new project
        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()

        flash("Project created successfully.", "success")
        return redirect(url_for("project.list_projects"))

    # Get all projects, newest first
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("projects.html", projects=projects)


