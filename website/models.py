from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as SQLEnum, Boolean, Text
import enum
import re


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Model(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  projectname = db.Column(db.String(255), nullable = False)
  model_weights_path = db.Column(db.String(255), nullable=True)
  requirements_path = db.Column(db.String(255), nullable=True)
  model_inference_path = db.Column(db.String(255), nullable=True) 
  inference_script_paths = db.Column(Text, nullable=True)

class Environment(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  modelname = db.Column(db.String(255), nullable = False)
  environment_name = db.Column(db.String(255), nullable = False)

class TransformerModel(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  benchmark = db.Column(db.String(255), nullable = False)
  model_name = db.Column(db.String(80), nullable=True)
  n_parameters = db.Column(db.String(10), nullable=True)    
  bleu = db.Column(db.Float, nullable=True)
  ter = db.Column(db.Float, nullable=True)  
  chrF = db.Column(db.Float, nullable=True)
  BERTScore = db.Column(db.Float, nullable=True)
  COMET = db.Column(db.Float, nullable=True)
  paper = db.Column(db.String, nullable=True)
  code = db.Column(db.String(80), nullable=True)
  year = db.Column(db.Integer, nullable=True)
  zip_file_path = db.Column(db.String(250), nullable=False)
  lang_pairs = db.Column(db.String(10), nullable=False)
  # rank = db.Column(db.Integer, nullable=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique = True, nullable=False)
    source_file_path = db.Column(db.String(250), nullable=False)
    target_file_path = db.Column(db.String(250), nullable=False)
    zip_file_path = db.Column(db.String(250), nullable=False)
    lang_pairs = db.Column(db.String(10), nullable=False)

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DEV = "dev"
    GUEST = "guest"

class Users(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(20), unique=True)
     password = db.Column(db.String(128), nullable = False)
     email = db.Column(db.String(128), nullable = False)
     first_name = db.Column(db.String(128), nullable = False)
     user_role = db.Column(SQLEnum(UserRole), nullable = False)
     isLoggedIn = db.Column(Boolean, default = False)

     def set_password(self, password):
         self.password = generate_password_hash(password)

     def check_password(self, password):
         print(password)
         print(self.password)
         return check_password_hash(self.password, password)

     def is_valid_email(self):
         """Simple email validation method."""
         regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
         return re.match(regex, self.email) is not None
    

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     notes = db.relationship('Note')