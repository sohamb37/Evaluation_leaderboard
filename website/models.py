from . import db
#from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class TransformerModel(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  training_data = db.Column(db.String(255))
  model_name = db.Column(db.String(80), nullable=True)
  n_parameters = db.Column(db.String(10), nullable=True)    
  bleu = db.Column(db.Float, nullable=True)
  ter = db.Column(db.Float, nullable=True)  
  chrF = db.Column(db.Float, nullable=True)
  BERTScore = db.Column(db.Float, nullable=True)
  COMET = db.Column(db.Float, nullable=True)
  paper = db.Column(db.String, nullable=True)
  code = db.Column(db.String(80), nullable=True)
  result = db.Column(db.String(80), nullable=True)
  year = db.Column(db.Integer, nullable=True)  
  # rank = db.Column(db.Integer, nullable=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Benchmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    file_path = db.Column(db.String(150), nullable=False)

    

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     notes = db.relationship('Note')