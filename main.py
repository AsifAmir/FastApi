from fastapi import Body, FastAPI

app = FastAPI()

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

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    print(f'Course Code: {payload["Course Code"]} Course Title: {payload["Course Title"]}')
    print(f'Course Credits: {payload["Course Credits"]}')

    return{"message": "Post created successfully", 
           "new_post": f"Course Code: {payload['Course Code']}, Course Title: {payload['Course Title']}, Course Credits: {payload['Course Credits']}"}