from flask import render_template , redirect , url_for , flash 
from flask_login import login_user
from . import auth_bp
from .forms import RegisterationForm , LoginForm
from app.models import User , Freelancer_profile , Client_profile
from app.extensions import db , bcrypt
@auth_bp.route("/register" , methods = ["GET","POST"])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash ("Email Already Registered. Please Login" , "danger")
            return redirect(url_for("auth.register"))
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed_password,
            role = form.role.data
        )
        
        db.session.add(user)
        db.session.flush()
        
        if user.role == "freelancer":
            profile = Freelancer_profile(
                user_id=user.id,
                skills=""
            )
        
        elif user.role == "client":
            profile = Client_profile(
                user_id=user.id,
                company_name = "New Company"
            )
            
        db.session.add(profile)
        db.session.commit()
        flash("Registeration Successful! Please Login" , "Success")
        return redirect(url_for("auth.login"))
        
    return render_template("register.html" , form=form)

@auth_bp.route("/login" , methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            if bcrypt.check_password_hash(existing_user.password , form.password.data):
                login_user(existing_user , remember=form.remember.data)
                flash("Login Sucessful" , "Success")
                return redirect(url_for("freelancer.dashboard"))              
            if existing_user.role == "freelancer":
                flash("Login Sucessful" , "Success")
                return redirect(url_for("freelancer.dashboard"))
            else:
                flash("Login Sucessful" , "Success")
                return redirect (url_for("client.dashboard"))
        flash("Invalid Email or Password" , "danger")
        return render_template("login.html" , form=form)
    
    return render_template("login.html" , form=form)