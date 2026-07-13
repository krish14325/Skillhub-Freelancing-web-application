from flask import Blueprint
freelancer_bp = Blueprint("freelancer_bp" , __name__ , url_prefix="/freelancer")
from . import routes