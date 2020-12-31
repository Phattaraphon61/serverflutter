from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel,Field
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import pymongo
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
import requests
import jwt
import os
import bcrypt
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