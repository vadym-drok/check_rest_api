from fastapi import FastAPI
from app.routers import users, receipts


app = FastAPI(docs_url='/')


app.include_router(receipts.router)
app.include_router(users.router)
