from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return{"message":"API is running"}

@app.get("/health")
def health():
    return{"Status":"Ok"}

@app.get("/echo")
def echo(message: str = "hello"):
    return{"echo":message}
