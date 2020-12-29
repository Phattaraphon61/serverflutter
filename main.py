from fastapi import FastAPI
from pydantic import BaseModel
from numpy import sign
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "*",
    "https://commath-phattaraphon.herokuapp.com",
    "https://commath-phattaraphon.herokuapp.com/b2s",
    "https://commath-phattaraphon.herokuapp.com/elimination",
    "https://commath-phattaraphon.herokuapp.com/interpolation",
    "https://commath-phattaraphon.herokuapp.com/differentiation",
    "https://commath-phattaraphon.herokuapp.com/integration",
    "https://commath-phattaraphon.herokuapp.com/root-finding"

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
    return {"22222"}