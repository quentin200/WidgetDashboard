from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def title():
    return {"message": "Personnal Widget Dashboard API"}

@app.get("/health")
def status():
    return {"status": "OK"}