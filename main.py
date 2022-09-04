from typing import List

import fastapi
import sqlalchemy.orm as orm

import schemas
import services
from database import DB

app = fastapi.FastAPI()
services.create_db()


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: orm.Session = fastapi.Depends(services.get_db)):
    db_user = services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail='“A user with that email already exists.')
    return services.create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: orm.Session = fastapi.Depends(services.get_db)):
    users = services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get('/user/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    user = services.get_user(db=db, user_id=user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail='not found')
    return user


@app.post('/user/{user_id}/posts/', response_model=schemas.Post)
def create_post(user_id: int, post: schemas.PostCreate, db: orm.Session = fastapi.Depends(services.get_db)):
    user = services.get_user(db=db, user_id=user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail='The user with this id does not exist.')
    return services.create_post(user_id=user_id, post=post, db=db)


@app.get('/posts/', response_model=List[schemas.Post])
def get_posts(skip: int = 0, limit: int = 10, db: orm.Session = fastapi.Depends(services.get_db)):
    posts = services.get_posts(db=db, skip=skip, limit=limit)
    return posts


@app.get('/post/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    post = services.get_post(db=db, post_id=post_id)
    if not post:
        raise fastapi.HTTPException(status_code=404, detail='not found')
    return post


@app.put('/post/{post_id}/', response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: orm.Session = fastapi.Depends(services.get_db)):
    services.update_post(post_id=post_id, post=post, db=db)
    return services.update_post(post_id=post_id, post=post, db=db)


@app.delete('/post/{post_id}')
def delete_post(post_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    services.delete_post(post_id=post_id, db=db)
    return {'message': f'You have deleted the post with id {post_id} successfully.'}


@app.post('/query/')
async def read_db(query: schemas.PostCreate):
    # print(query.__dict__)
    # print(query.title)
    # print(query.content)
    data = await DB.fetch_all("SELECT * FROM user")
    return data
