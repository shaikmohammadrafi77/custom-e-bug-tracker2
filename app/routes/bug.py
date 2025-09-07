# app/routes/bug.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required, current_user
from app.models import Bug, Project
from app import db
from app.ai_engine import analyze_and_fix_code
from io import BytesIO
import traceback

# Blueprint definition
bug_bp = Blueprint("bug", __name__)

# -------------------------
# Report a new bug
# -------------------------
@bug_bp.route("/report", methods=["GET", "POST"])
@login_required
def report_bug():
    try:
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            code = request.form.get("code")
            project_id = request.form.get("project_id")
            
            # Basic validation
            if not title or not description:
                flash("Title and description are required.", "error")
                return render_template("report_bug.html", projects=Project.query.all())
            
            # Create new bug entry
            new_bug = Bug(
                title=title,
                description=description,
                code_snippet=code,
                user_id=current_user.id,
                project_id=project_id
            )
            
            db.session.add(new_bug)
            db.session.commit()
            
            # Try to generate AI fix if code is provided
            if code:
                try:
                    ai_result = analyze_and_fix_code(code, description)
                    new_bug.fixed_code = ai_result.get('fixed_code', '')
                    new_bug.ai_notes = ai_result.get('ai_notes', 'AI analysis failed')
                    db.session.commit()
                except Exception as ai_error:
                    print(f"AI analysis failed: {ai_error}")
                    # Continue even if AI fails
            
            flash("Bug reported successfully.", "success")
            return redirect(url_for("bug.bug_detail", bug_id=new_bug.id))
        
        # GET request - show form with projects
        projects = Project.query.filter_by(creator_id=current_user.id).all()
        return render_template("report_bug.html", projects=projects)
    
    except Exception as e:
        print(f"Error in report_bug: {e}")
        traceback.print_exc()
        flash("An error occurred while reporting the bug.", "error")
        return redirect(url_for("dashboard.index"))

# -------------------------
# Bug detail page
# -------------------------
@bug_bp.route("/<int:bug_id>")
@login_required
def bug_detail(bug_id):
    try:
        bug = Bug.query.get_or_404(bug_id)
        
        # Verify user has access to this bug
        if bug.user_id != current_user.id and not current_user.is_admin:
            flash("You don't have permission to view this bug.", "error")
            return redirect(url_for("bug.bug_list"))
        
        return render_template("bug_detail.html", bug=bug)
    
    except Exception as e:
        print(f"Error in bug_detail: {e}")
        flash("An error occurred while loading the bug details.", "error")
        return redirect(url_for("bug.bug_list"))

# -------------------------
# List all bugs for current user
# -------------------------
@bug_bp.route("/list")
@login_required
def bug_list():
    try:
        if current_user.is_admin:
            bugs = Bug.query.all()
        else:
            bugs = Bug.query.filter_by(user_id=current_user.id).all()
        
        return render_template("bug_list.html", bugs=bugs)
    
    except Exception as e:
        print(f"Error in bug_list: {e}")
        flash("An error occurred while loading bugs.", "error")
        return redirect(url_for("dashboard.index"))

# -------------------------
# AI fix for bug code
# -------------------------
@bug_bp.route("/<int:bug_id>/ai_fix")
@login_required
def ai_fix(bug_id):
    try:
        bug = Bug.query.get_or_404(bug_id)
        
        # Verify user has access to this bug
        if bug.user_id != current_user.id and not current_user.is_admin:
            flash("You don't have permission to modify this bug.", "error")
            return redirect(url_for("bug.bug_list"))
        
        # Check if there's code to analyze
        if not bug.code_snippet:
            flash("No code available to analyze.", "warning")
            return redirect(url_for("bug.bug_detail", bug_id=bug_id))
        
        # Analyze and fix code using AI
        ai_result = analyze_and_fix_code(bug.code_snippet, bug.description)
        
        # Update bug with AI results
        bug.fixed_code = ai_result.get('fixed_code', '')
        bug.ai_notes = ai_result.get('ai_notes', 'AI analysis completed')
        bug.status = "Fixed"
        db.session.commit()
        
        flash("AI attempted a fix for this bug.", "success")
        return redirect(url_for("bug.bug_detail", bug_id=bug_id))
    
    except Exception as e:
        print(f"Error in ai_fix: {e}")
        traceback.print_exc()
        flash("An error occurred during AI analysis.", "error")
        return redirect(url_for("bug.bug_detail", bug_id=bug_id))

# -------------------------
# Download bug code
# -------------------------
@bug_bp.route("/<int:bug_id>/download")
@login_required
def download_bug_code(bug_id):
    try:
        bug = Bug.query.get_or_404(bug_id)
        
        # Verify user has access to this bug
        if bug.user_id != current_user.id and not current_user.is_admin:
            flash("You don't have permission to download this code.", "error")
            return redirect(url_for("bug.bug_list"))
        
        # Use fixed code if available, otherwise original code
        code = bug.fixed_code or bug.code_snippet or ""
        
        if not code:
            flash("No code available to download.", "warning")
            return redirect(url_for("bug.bug_detail", bug_id=bug_id))
        
        # Create in-memory file
        data = BytesIO(code.encode("utf-8"))
        
        return send_file(
            data,
            download_name=f"bug_{bug.id}_{bug.title.replace(' ', '_')}.py",
            as_attachment=True,
            mimetype="text/x-python"
        )
    
    except Exception as e:
        print(f"Error in download_bug_code: {e}")
        flash("An error occurred while downloading the code.", "error")
        return redirect(url_for("bug.bug_detail", bug_id=bug_id))

# -------------------------
# API endpoint for real-time AI code analysis
# -------------------------
@bug_bp.route("/api/analyze_code", methods=["POST"])
@login_required
def analyze_code_api():
    try:
        data = request.get_json()
        code = data.get("code", "")
        description = data.get("description", "")
        
        result = analyze_and_fix_code(code, description)
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in analyze_code_api: {e}")
        return jsonify({
            "fixed_code": code,
            "ai_notes": "Error in AI analysis",
            "error": str(e)
        }), 500