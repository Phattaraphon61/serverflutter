from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel,Field,BaseConfig
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


cluster = MongoClient('mongodb+srv://phattaraphon:0989153312@cluster0.trckf.mongodb.net/flutter?retryWrites=true&w=majority')
# cluster = MongoClient('mongodb://localhost:27017')

db = cluster["flutter"]
collection = db['test']
dbUser = db['User'] 

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

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')
# class Users(BaseModel):
#     id: Optional[PyObjectId] = Field(alias='_id')
#     tt: Optional[PyObjectId] = Field(alias='id')
#     image: str
#     # email:str
#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: str
#         }


class MongoBase(BaseModel):
    id: Optional[PyObjectId]
    tt:Optional[PyObjectId]
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

    def __init__(self, **pydict):
        super().__init__(**pydict)
        self.id = pydict.get('_id')
        self.tt = pydict.get('id')

class Users(MongoBase):
    image: str



class Singup(BaseModel):
    name: str
    email:str
    password: str
class Singin(BaseModel):
    email:str
    password: str    
class CheckEmail(BaseModel):
    email:str 

@app.get("/")
def home():
    return {"999"}
@app.get("/getdata/{id}")
async def read_root(id:str):
    tt = []
    for i in collection.find({'id':id}):
        print(i)
        tt.append(Users(**i))
    if len(tt) == 0:

        return [{'_id':"99",'id': "55",'image':'88'}]  
    return tt
@app.post("/singin")
async def singin(tt:Singin):
    email = tt.email
    password = tt.password.encode("utf-8")
    user = dbUser.find({'email':email})
    try :
        yy = user[0]['email']
        try:
            passdb = user[0]['password'].encode('utf-8')
            if bcrypt.checkpw(password,passdb):
                print("match")
                ids = str(user[0]['_id'])
                name = str(user[0]['name'])
                email = str(user[0]['email'])
                token = jwt.encode({'id': ids, 'name': name,'email': email},key="",algorithm="HS256")
                return {'status':'singin success'}
                # return {'status':'singin success','token':token}
            else:
                print("does not match")
                return {'status':'password is incorrectsssss'}
        except:
            return {'status':'password is incorrect'}
            
    except:
        return {'status':'invalid email'}

@app.post("/singup")
async def singup(tt:Singup):
    name = tt.name
    email = tt.email
    password = tt.password.encode('utf-8')
    checkemail = dbUser.find({'email': email})

    try:
        yy = checkemail[0]
        print("มี")
        return "this email has already been used"
    except:
        print("ไม่มี")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        p = hashed.decode()
        dbUser.insert_one({'name':name,'email':email,'password':p})
        return "success"
@app.post("/checkemail")
async def singup(tt:CheckEmail):
    email = tt.email
    print(email)
    checkemail = dbUser.find({'email': email})

    try:
        yy = checkemail[0]
        print("มี")
        return "this email has already been used"
    except:
        print("ไม่มี")
        return "success"

@app.post("/files/{id}/")
def create_upload_file(id:str,file: UploadFile = File(...)):
    collection.insert_one({'id':id,'image':file.filename})
    fn = os.path.basename(file.filename)
    open("files/"+fn,'wb').write(file.file.read())
    file_like = open("files/"+fn,"rb")
    return StreamingResponse(file_like, media_type="image/jpg")


@app.get("/getimage/{name}")
def getimages(name:str):
    file_like = open("files/"+name, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")
