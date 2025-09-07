# app/routes/dashboard.py
from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Bug    # use absolute import
from app import db            # use absolute import

# Blueprint definition
dashboard_bp = Blueprint("dashboard", __name__)

# -------------------------
# Dashboard route
# -------------------------
@dashboard_bp.route("/dashboard")
@login_required
def index():
    # Fetch latest 20 bugs
    bugs = Bug.query.order_by(Bug.created_at.desc()).limit(20).all()
    return render_template("dashboard.html", bugs=bugs)

