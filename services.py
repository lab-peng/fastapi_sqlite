import sqlalchemy.orm as orm

import database
import schemas
from models import User


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
