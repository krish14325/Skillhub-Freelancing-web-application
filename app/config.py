import os 

class Config:
    SECRET_KEY = "skill_hub_secret_key"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sqlroot2008#@localhost/skillhub" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join("static","uploads") 
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    