from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    Course_Code: str
    Course_Title: Optional[str] = None
    Course_Credits: int
    Enrolled: bool = True

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

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     print(f'Course Code: {payload["Course_Code"]} Course Title: {payload["Course_Title"]}')
#     print(f'Course Credits: {payload["Course_Credits"]}')

#     return{"message": "Post created successfully", 
#            "new_post": f"Course Code: {payload['Course_Code']}, Course Title: {payload['Course_Title']}, Course Credits: {payload['Course_Credits']}"}


@app.post("/createposts")
def create_posts(payload: Post): # Using Pydantic model to validate the incoming data
    print(payload)
    payload_dict = payload.dict() # Convert the Pydantic model to a dictionary
    print(payload_dict)

    # print(f'Course Code: {payload.Course_Code}, Course Title: {payload.Course_Title}, Course Credits: {payload.Course_Credits}')
    # print(f'Enrolled: {payload.Enrolled}')
    # return {"data": "This is your posts"}
    # return{f'Course Code: {payload.Course_Code}, Course Title: {payload.Course_Title}, Course Credits: {payload.Course_Credits}, Enrolled: {payload.Enrolled}'}
    # return{f'Enrolled: {payload.Enrolled}'}
    # return{f'Course Title: {payload.Course_Title}'}
    return{"data": payload_dict}