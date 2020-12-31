from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import pymongo
from pymongo import MongoClient
app = FastAPI()
origins = [
    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"555"}