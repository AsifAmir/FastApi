from fastapi import FastAPI

app = FastAPI()

# 1. The Decorator
@app.get("/")
# 2. The Path Operation Function
def root():
    return {"message": "Hello World"}

# 1. The Decorator
@app.get("/login")
# 2. The Path Operation Function
def login():
    return {"message": "Login Page"}