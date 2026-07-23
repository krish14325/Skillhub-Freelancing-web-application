from app.extensions import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin , db.Model):
    __tablename__ = "users"
    
    id =       db.Column(db.Integer , primary_key = True , unique = True)
    
    username = db.Column(db.String(100) , nullable = False)

    email =    db.Column(db.String(150) , unique = True , nullable = False)

    password = db.Column(db.String(255) , nullable = False)

    role =     db.Column(db.String(20) , nullable = False)
    
    created_at=db.Column(db.DateTime , default = datetime.utcnow)

    freelancer_profile = db.relationship("Freelancer_profile" , back_populates="user" , uselist = False)

    client_profile = db.relationship("Client_profile" , back_populates="user" , uselist = False)
    
class Freelancer_profile(db.Model):
    __tablename__ = "freelancerprofiles"
    
    id = db.Column(db.Integer  , primary_key = True , unique = True)
    
    user_id = db.Column(db.Integer , db.ForeignKey("users.id") , unique=True , nullable = False)
    
    skills = db.Column(db.Text)
    
    full_name = db.Column(db.String(100))
    
    bio = db.Column(db.Text)
    
    experience = db.Column(db.String(100))
    
    education = db.Column(db.String(150))
    
    hourly_rate = db.Column(db.Integer)

    country = db.Column(db.String(100))
    
    city = db.Column(db.String(100))
    
    linkedin = db.Column(db.String(200))
    
    github = db.Column(db.String(200))
    
    portfolio = db.Column(db.String(200))
    
    user = db.relationship("User" , back_populates="freelancer_profile")
    
    services = db.relationship("Service" , back_populates = "freelancer" , cascade = "all, delete-orphan")

class Client_profile(db.Model):
    __tablename__ = "client_profiles"

    id = db.Column(db.Integer  , primary_key = True , unique =True)
    
    user_id = db.Column(db.Integer , db.ForeignKey("users.id") , unique=True , nullable = False)
    
    company_name = db.Column(db.String(150) , nullable = False)
    
    company_logo = db.Column(db.String(255))
    
    website = db.Column(db.String(200))
    
    description = db.Column(db.Text)
    
    user = db.relationship("User" , back_populates="client_profile")
    
    orders = db.relationship(
    "Order",
    back_populates="client",
    cascade="all, delete-orphan"
                )
    
class Service(db.Model):
    __tablename__ = "services"
    
    id = db.Column(db.Integer  , primary_key = True ,unique = True)
    
    freelancer_id = db.Column(db.Integer , db.ForeignKey("freelancerprofiles.id") , nullable = False)
    
    title = db.Column(db.String(155) , nullable = False)
    
    description = db.Column(db.String(155) , nullable = False)
    
    price = db.Column(db.Integer, nullable = False)

    delivery_time = db.Column(db.Integer , nullable = False)
    
    category = db.Column(db.String(100) , nullable = False)
    
    service_image = db.Column(db.String(100) , nullable = False)
    
    status = db.Column(db.String(20) , default="active")
    
    created_at = db.Column(db.DateTime , default= datetime.utcnow)
    
    freelancer = db.relationship("Freelancer_profile" , back_populates = "services")
    
    orders = db.relationship(
    "Order",
    back_populates="service",
    cascade="all, delete-orphan"
            )
    
class Order(db.Model):
    __tablename__ = "orders"
    
    id = db.Column(db.Integer , primary_key = True , unique = True)
    
    client_id = db.Column(
                        db.Integer , 
                        db.ForeignKey("client_profiles.id") ,
                        nullable = False
                        )
    
    service_id = db.Column(
                        db.Integer , 
                        db.ForeignKey("services.id") ,
                        nullable = False
                        )
    
    price_at_purchase = db.Column(db.Integer ,nullable = False )
    
    status = db.Column(db.String(20) , default = "Pending")
    
    ordered_at = db.Column(db.DateTime , default = datetime.utcnow)
    
    completed_at = db.Column(db.DateTime)
    
    delivered_file = db.Column(db.String(255))
    
    delivered_at = db.Column(db.DateTime)
    
    review = db.relationship("Review" , back_populates="order" , uselist=False , cascade = "all , delete-orphan")
    
    client = db.relationship(
    "Client_profile",
    back_populates="orders"
                            )

    service = db.relationship(
    "Service",
    back_populates="orders"
                    )
    
class Review(db.Model):
    __tablename__ = "reviews"
    
    id = db.Column(db.Integer , primary_key = True , unique= True)
    
    order_id = db.Column(db.Integer , db.ForeignKey("orders.id") , nullable=False , unique = True)
    
    rating = db.Column(db.Integer , nullable = False)
    
    comment = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime , default=datetime.utcnow)
    
    order = db.relationship("Order" ,  back_populates = "review")
    
