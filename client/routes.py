from . import client
from flask import render_template , redirect , url_for ,flash
from app.extensions import db
from app.models import *
from flask_login import login_required , current_user
from .forms import ProfileForm
@client.route("/dashboard")
@login_required
def dashboard():
    flash("login Successsfully!","success")
    return render_template("client_dashboard.html")

@client.route("/profile" , methods=["GET","POST"])
@login_required
def profile():
    form = ProfileForm()
    client_id = Client_profile.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        client_id.company_name = form.company_name.data
        client_id.company_logo = form.company_logo.data
        client_id.website = form.website.data
        client_id.description = form.description.data
        
        db.session.commit()
        flash("Profile Created Successfully" , "success")
        return redirect(url_for("Client.dashboard"))
    return render_template("client_profile.html" , form=form)
        
