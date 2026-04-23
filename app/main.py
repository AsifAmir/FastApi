from fastapi import FastAPI, Response, status, HTTPException, Depends
# Importing the routers for the API
from routers import posts, users, auth, vote
# Importing the database connection and models for SQLAlchemy
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db, cursor, conn

# Create the tables in the database based on the models defined in models.py
# models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

# ============= psycopg2 =============
# Raw sQL queries using psycopg2 adapter for PostgreSQL database connection.
# ====================================

# 1. The Decorator -> @app.get("/") -> HTTP method + path
# 2. path operation function -> root() -> function that is executed when the path is accessed
@app.get("/")
# 2. The Path Operation Function
def root():
    return {"message": "Hello World"}


@app.get("/test/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    data = cursor.fetchall()
    print(data)
    return({"data": data})


@app.post("/test/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    if not new_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post could not be created")
    return({"data": new_post})


@app.get("/test/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}


@app.delete("/test/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/test/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: schemas.PostUpdate):
    cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"data": updated_post}


#============= ORM Notes =============
# Object Relational Mapper (ORM) -> SQLAlchemy, Tortoise, Django ORM
# ORMs allow us to interact with the database using Python code instead of writing raw SQL queries. They provide an abstraction layer that simplifies database operations and can help prevent SQL injection attacks.
# ====================================
@app.get("/orm")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

# routes for posts and users are defined in separate files in the routers directory. 
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)