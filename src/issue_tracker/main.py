from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from issue_tracker.db.db_connect import db_connect
from issue_tracker.handlers.exception_handlers import validation_exception_handler
from issue_tracker.routes import auth_route, user_profile_route

app = FastAPI(
    title="Issue Tracker",
    description="A simple issue tracker",
    version="0.1.0",
    lifespan=db_connect,
)


app.exception_handler(RequestValidationError)(validation_exception_handler)


app.include_router(auth_route.router)
app.include_router(user_profile_route.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
