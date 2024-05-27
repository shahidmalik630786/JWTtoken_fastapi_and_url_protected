from fastapi import FastAPI
from models import Base,engine
from routers import authentication


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(authentication.router)