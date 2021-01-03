import pymongo
from pymongo import MongoClient


cluster = MongoClient('mongodb+srv://phattaraphon:0989153312@cluster0.trckf.mongodb.net/flutter?retryWrites=true&w=majority')
# cluster = MongoClient('mongodb://localhost:27017')

db = cluster["flutter"]
collection = db['test']

post ={"id":"dfsfsdfsfsd",'image':"sdfsdf.jpg"}
collection.insert_one(post)