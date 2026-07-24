from . import client
from flask import render_template , redirect , url_for ,flash , send_from_directory , current_app
from app.extensions import db
from app.models import *
from flask_login import login_required , current_user
from .forms import ProfileForm , ReviewForm
import os
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
        
@client.route("/hire/<int:service_id>")
@login_required
def hire(service_id):
    services = Service.query.get_or_404(service_id)
    client = Client_profile.query.filter_by(user_id = current_user.id).first()
    order = Order(
        client_id = client.id,
        service_id = services.id,
        price_at_purchase = services.price
    )
    db.session.add(order)
    db.session.commit()
    flash("Order Created Successfully!" , "success")
    return redirect(url_for("Client.dashboard"))

@client.route("/My_Orders", methods=["GET" , "POST"])
@login_required
def my_orders():
    client = Client_profile.query.filter_by(user_id=current_user.id).first()
    my_order = Order.query.filter_by(client_id = client.id).all()
    return render_template("myorders.html" , orders = my_order)

@client.route("/review/<int:order_id>" , methods=["GET" , "POST"])
@login_required
def review(order_id):
    order = Order.query.get_or_404(order_id)
    form = ReviewForm()
    if order.client.user_id != current_user.id:
        flash("Unauthorised User Access" , "danger")
        return redirect(url_for("Client.my_orders"))
    
    if order.status != "Completed":
        flash("You Can Only Review Completed Orders"  , "danger")
        return (redirect(url_for("Client.my_orders")))
    
    if order.review is not None:
        flash("You  Review Completed Orders"  , "danger")
        return (redirect(url_for("Client.my_orders")))
    if form.validate_on_submit():
        rating = Review(
            order_id = order_id,
            rating = int(form.rating.data),
            comment = form.comment.data,
        )
        db.session.add(rating)
        db.session.commit()
        flash("Thanks For Giving Your Review" , "success")
        return redirect(url_for("Client.my_orders"))
    
    return render_template("review.html" , form=form , order=order)
    
@client.route("/download/<int:order_id>")
@login_required
def download_project(order_id):
    order = Order.query.get_or_404(order_id)
    if order.client.user_id != current_user.id:
        flash("Unauthorised User","danger")
        return redirect(url_for("Client.dashboard"))
    upload_path = os.path.join(current_app.root_path,".." , "static","uploads")
    return send_from_directory(
        upload_path,
        order.delivered_file,
        as_attachment = True
    )
    

    