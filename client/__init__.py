from flask import Blueprint
client = Blueprint("Client",__name__,url_prefix="/client")
from . import routes