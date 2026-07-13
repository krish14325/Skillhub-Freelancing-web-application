from flask import render_template
from flask_login import login_required , current_user
from . import freelancer_bp

@freelancer_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("freelancer_dashboard.html")
