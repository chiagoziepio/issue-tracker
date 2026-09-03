# from contextlib import asynccontextmanager

# from fastapi import FastAPI

# from issue_tracker.db.base import Base
# from issue_tracker.db.session import engine


# @asynccontextmanager
# async def db_connect(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         yield

#     await engine.dispose()


from contextlib import asynccontextmanager

from fastapi import FastAPI

from issue_tracker.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await engine.dispose()
