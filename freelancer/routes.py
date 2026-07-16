from flask import render_template , redirect , url_for , flash 
from flask_login import login_required , current_user
from . import freelancer_bp
from .forms import ProfileForm , ServiceForm
from app.models import Freelancer_profile , Service
from app.extensions import db

@freelancer_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("freelancer_dashboard.html")

@freelancer_bp.route("/profile" , methods=["GET" , "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Freelancer_profile.query.filter_by(user_id=current_user.id).first()
        profile.full_name = form.full_name.data
        profile.bio = form.Bio.data
        profile.skills = form.skills.data
        profile.experience = form.experience.data
        profile.education = form.education.data
        profile.hourly_rate = form.hourly_rate.data
        profile.country = form.country.data
        profile.city = form.city.data
        profile.linkedin = form.linkedin.data
        profile.portfolio = form.portfolio.data
        profile.github = form.github.data
        db.session.commit()
        flash("Profile Updated Successfully!" , "success")
        return redirect(url_for("freelancer_bp.dashboard"))
    profile = Freelancer_profile.query.filter_by(user_id=current_user.id).first()
    form.full_name.data = profile.full_name
    form.Bio.data = profile.bio
    form.skills.data = profile.skills 
    form.experience.data = profile.experience 
    form.education.data = profile.education  
    form.hourly_rate.data = profile.hourly_rate 
    form.country.data = profile.country 
    form.city.data = profile.city  
    form.linkedin.data = profile.linkedin  
    form.portfolio.data = profile.portfolio  
    form.github.data = profile.github  
    return render_template("freelancer_profile.html" , form=form)

@freelancer_bp.route("/add_service" , methods=["GET" , "POST"])
@login_required
def add_service():
    profile = Freelancer_profile.query.filter_by(user_id = current_user.id).first()
    if profile is None:
        flash("Please Complete Your PRofile First." , "danger")
        return redirect(url_for("freelancer_bp.profile"))
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            freelancer_id = profile.id,
            title = form.title.data,
            description = form.description.data,
            price = form.price.data,
            delivery_time = form.delivery_time.data,
            category = form.category.data,
            service_image = form.service_image.data
        )
        db.session.add(service)
        db.session.commit()
        flash("Service Added Successfully!" , "success")
        return redirect(url_for("freelancer_bp.dashboard"))
    return render_template("add_service.html" , form=form)
    