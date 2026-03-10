from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -------------------------
# Q1: Basic Home Route
# -------------------------
@app.get("/")
def home():
    return {"message": "FastAPI Assignment Running Successfully"}


# -------------------------
# Q2: Add Two Numbers
# Example: /add?a=5&b=10
# -------------------------
@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}


# -------------------------
# Q3: Square of a Number (Path Parameter)
# Example: /square/4
# -------------------------
@app.get("/square/{num}")
def square(num: int):
    return {"number": num, "square": num * num}


# -------------------------
# Q4: Create User (POST Request)
# -------------------------

class User(BaseModel):
    name: str
    age: int


@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "User Created Successfully",
        "user_details": user
    }


# -------------------------
# Q5: Simple Calculator
# Example: /calculate?a=10&b=2&operation=mul
# -------------------------
@app.get("/calculate")
def calculate(a: int, b: int, operation: str):
    
    if operation == "add":
        result = a + b
    elif operation == "sub":
        result = a - b
    elif operation == "mul":
        result = a * b
    elif operation == "div":
        if b == 0:
            return {"error": "Division by zero not allowed"}
        result = a / b
    else:
        return {"error": "Invalid operation"}

    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }