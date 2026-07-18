from . import client
from flask import render_template , redirect , url_for ,flash
from app.extensions import db
from app.models import *
from flask_login import login_required , current_user
from .forms import ProfileForm
@client.route("/dashboard")
@login_required
def dashboard():
    services = Service.query.filter_by(status="active").all()
    return render_template("client_dashboard.html", services=services)

@client.route("/profile" , methods=["GET","POST"])
@login_required
def profile():
    form = ProfileForm()
    profile = Client_profile.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        profile.company_name = form.company_name.data
        profile.company_logo = form.company_logo.data
        profile.website = form.website.data
        profile.description = form.description.data
        db.session.commit()
        flash("Profile Created Successfully" , "success")
        return redirect(url_for("Client.dashboard"))
    form.company_name.data = profile.company_name
    form.company_logo.data = profile.company_logo
    form.website.data = profile.website
    form.description.data = profile.description
    return render_template("client_profile.html" , form=form)

@client.route("/services/<int:service_id>")
@login_required
def services(service_id):
    service = Service.query.get_or_404(service_id)
    return render_template("service_detail.html" , service=service)
        
