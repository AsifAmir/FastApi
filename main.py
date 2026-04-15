import os
from time import sleep
from typing import Optional
from random import randrange
from fastapi import Body, FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
# Load variables from .env into the environment
load_dotenv()

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        sleep(2)


# decorator -> @app.get("/") -> HTTP method + path
# path operation function -> root() -> function that is executed when the path is accessed

# 1. The Decorator
@app.get("/")
# 2. The Path Operation Function
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    data = cursor.fetchall()
    return(data)

