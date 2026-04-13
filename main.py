from typing import Optional
from random import randrange
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()
posts = []
class Post(BaseModel):
    Course_Code: str
    Course_Title: Optional[str] = None
    Course_Credits: int
    Enrolled: bool = False

# decorator -> @app.get("/") -> HTTP method + path
# path operation function -> root() -> function that is executed when the path is accessed

# 1. The Decorator
@app.get("/")
# 2. The Path Operation Function
def root():
    return {"message": "Hello World"}

@app.get("/login")
def login():
    return {"message": "Login Page"}



@app.post("/posts")
def create_posts(payload: Post): # Using Pydantic model to validate the incoming data
    # print(payload)
    payload_dict = payload.dict() # Convert the Pydantic model to a dictionary
    payload_dict['id'] = randrange(0, 1000000) # Add a random id to the payload dictionary
    print(payload_dict)
    posts.append(payload_dict) # Add the new post to the list of posts
    print(posts)
    # return{"message": "Post created successfully","data": payload_dict,
    #        "post": f"Course Code: {payload_dict['Course_Code']}, Course Title: {payload_dict['Course_Title']}, Course Credits: {payload_dict['Course_Credits']}, Enrolled: {payload_dict['Enrolled']}"}
    return {"message": "Post created successfully", "data": payload_dict}