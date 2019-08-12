from sqlalchemy.sql import func, desc
from config import db
likes_table = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('quote_id', db.Integer, db.ForeignKey('quotes.id'), primary_key=True))
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    quotes_this_user_likes = db.relationship('Quote', secondary=likes_table)
class Quote(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author =  db.Column(db.String(255))
    quote =  db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user = db.relationship('User', foreign_keys=[user_id], backref="user_quotes")
    users_who_like_this_quote = db.relationship('User', secondary=likes_table)