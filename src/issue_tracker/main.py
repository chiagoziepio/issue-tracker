from fastapi import FastAPI

app = FastAPI(
    title="Issue Tracker",
    description="A simple issue tracker",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
