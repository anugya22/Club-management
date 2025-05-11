from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)

    # Flask-Login properties
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Relationships
    proposals = db.relationship("Proposal", backref="user", lazy=True)
    created_events = db.relationship("EventClub", backref="creator", lazy=True)
    
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    sales = db.Column(db.Float, default=0.0)


    def __init__(self, name, price, sales=0):
        self.name = name
        self.price = price
        self.sales = sales




class Proposal(db.Model):
    __tablename__ = "proposals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # User relationship already defined in User class


class EventClub(db.Model):
    __tablename__ = "eventclub"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # User relationship already defined in User class
