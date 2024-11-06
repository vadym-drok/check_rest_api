from fastapi import FastAPI
from app import routers


app = FastAPI(docs_url='/')


app.include_router(routers.router)


# Initialize database
def init_db():
    from app.database import engine, Base
    Base.metadata.create_all(bind=engine)


init_db()
