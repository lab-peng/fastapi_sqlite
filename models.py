from email.policy import default
import datetime

import sqlalchemy as sql
import sqlalchemy.orm as orm

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    hashed_password = sql.Column(sql.String)
    is_active = sql.Column(sql.Boolean, default=True)

    posts = orm.relationship("Post", back_populates='owner')


class Post(Base):
    __tablename__ = 'post'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    title = sql.Column(sql.String, index=True)
    content = sql.Column(sql.String, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'))
    date_created = sql.Column(sql.DateTime, default=datetime.datetime.now)
    date_updated = sql.Column(sql.DateTime, default=datetime.datetime.now)

    owner = orm.relationship("User", back_populates='posts')
