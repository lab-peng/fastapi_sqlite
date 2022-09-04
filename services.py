import datetime

import sqlalchemy.orm as orm

import database
import schemas
from models import User, Post


def create_db():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: orm.Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: orm.Session, user: schemas.UserCreate):
    hashed_password = user.password + 'thisisnotsecure'
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: orm.Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: orm.Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_post(db: orm.Session, post: schemas.PostCreate, user_id: int):
    print(post.dict())
    db_post = Post(owner_id=user_id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: orm.Session, skip: int, limit: int):
    return db.query(Post).offset(skip).limit(limit).all()


def get_post(db: orm.Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def update_post(db: orm.Session, post: schemas.PostCreate, post_id: int):
    db_post = get_post(db=db, post_id=post_id)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_updated = datetime.datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post






def delete_post(db: orm.Session, post_id: int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
