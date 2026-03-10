from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Assignment Running"}

@app.get("/hello")
def hello():
    return {"message": "Hello World"}

@app.get("/add/{a}/{b}")
def add_numbers(a: int, b: int):
    return {"sum": a + b}

@app.get("/square/{num}")
def square(num: int):
    return {"number": num, "square": num * num}