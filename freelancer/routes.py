from flask import render_template , redirect , url_for , flash , current_app 
from flask_login import login_required , current_user
from . import freelancer_bp
from .forms import ProfileForm , ServiceForm , UploadForm
from app.models import Freelancer_profile , Service , Order
from app.extensions import db
from datetime import datetime
import os 
from werkzeug.utils import secure_filename 
import uuid

@freelancer_bp.route("/dashboard")
@login_required
def dashboard():
    profile = Freelancer_profile.query.filter_by(user_id=current_user.id).first()
    services = Service.query.filter_by(freelancer_id = profile.id).all()
    return render_template("freelancer_dashboard.html" , services=services)

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

@freelancer_bp.route("/edit_service/<int:service_id>" , methods=["GET" , "POST"])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        service.price = form.price.data
        service.delivery_time = form.delivery_time.data
        service.category = form.category.data
        service.service_image = form.service_image.data
        db.session.commit()
        flash("Service Updated Successfully" , "success")
        return redirect(url_for("freelancer_bp.dashboard"))
    form.title.data = service.title
    form.description.data = service.description
    form.price.data = service.price
    form.delivery_time.data = service.delivery_time
    form.category.data = service.category
    form.service_image.data = service.service_image
    return render_template("add_service.html" , form=form)

@freelancer_bp.route("/delete_service/<int:service_id>")
@login_required
def delete(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Service Deleted Successfully!","success")
    return redirect(url_for("freelancer_bp.dashboard"))

@freelancer_bp.route("/orders")
@login_required
def freelancer_orders():
    profile = Freelancer_profile.query.filter_by(user_id = current_user.id).first()
    orders = []
    for service in profile.services:
        orders.extend(service.orders)
        
    return render_template("freelancer_orders.html" , orders=orders)

@freelancer_bp.route("/order/<int:order_id>")
@login_required
def order_details(order_id):
    order_detail = Order.query.get_or_404(order_id)
    return render_template("order_detail.html" , order=order_detail)

@freelancer_bp.route("/accept/<int:order_id>")
@login_required
def accept_order(order_id):
    profile = Freelancer_profile.query.filter_by(user_id = current_user.id).first()
    order = Order.query.get_or_404(order_id)
    if order.service.freelancer_id != profile.id:
        flash("Unauthorised Access" , "success")
        return redirect(url_for("freelancer_bp.freelancer_orders"))
    if order.status!="Pending":
        flash("This Order Has Already Been Processed" , "danger")
        return redirect(url_for("freelancer_bp.freelancer_orders"))
    order.status = "Accepted"
    db.session.commit()
    flash("Order Accepted" , "success")
    return redirect(url_for("freelancer_bp.freelancer_orders"))

@freelancer_bp.route("/reject/<int:order_id>")
@login_required
def reject_order(order_id):
    profile = Freelancer_profile.query.filter_by(user_id = current_user.id).first()
    order = Order.query.get_or_404(order_id)
    if order.service.freelancer_id != profile.id:
        flash("Unauthorised Access" , "success")
        return redirect(url_for("freelancer_bp.freelancer_orders"))

    if order.status!="Pending":
        flash("This Order Has Already Been Processed" , "danger")
        return redirect(url_for("freelancer_bp.freelancer_orders"))
    
    order.status = "Rejected"
    db.session.commit()
    flash("Order Rejected" , "success")
    return redirect(url_for("freelancer_bp.freelancer_orders"))

@freelancer_bp.route("/completed/<int:order_id>")
@login_required
def completed(order_id):
    profile = Freelancer_profile.query.filter_by(user_id = current_user.id).first()
    order = Order.query.get_or_404(order_id)
    if order.service.freelancer_id != profile.id:
        flash("Unauthorised Access" , "success")
        return redirect(url_for("freelancer_bp.freelancer_orders"))

    if order.status!="Accepted":
        flash("Only Accepted Orders Can Be Marked As Completed" , "danger")
        return redirect(url_for("freelancer_bp.freelancer_orders"))
    else:
        order.status = "Completed"
        order.completed_at = datetime.utcnow()
        db.session.commit()
        flash("Order Completed " , "success")
        return redirect(url_for("freelancer_bp.order_details" , order_id=order.id))

@freelancer_bp.route("/deliver/<int:order_id>" , methods=["GET","POST"])
@login_required
def deliver(order_id):
    order = Order.query.get_or_404(order_id)
    form = UploadForm()
    if form.validate_on_submit():
        project = form.project_file.data
        filename = secure_filename(project.filename)
        unique_filename =  f"{order.id}_{filename}"
        project.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"] , unique_filename
            )
        )
        order.delivered_file = unique_filename
        order.delivered_at = datetime.utcnow()
        order.status = "Completed"
        print("inside deliver")
        db.session.commit()
        flash("Project delivered successfully" , "success")
        return redirect(url_for("freelancer_bp.freelancer_orders"))
    else:
        print(form.errors)
    return render_template("deliver_upload.html",form=form , order=order)

