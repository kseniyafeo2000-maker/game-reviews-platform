from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Мой первый FastAPI проект работает!"}

@app.get("/health")
def health():
    return {"status": "ok"}