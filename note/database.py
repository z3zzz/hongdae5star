from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.get_database('user')

notes = db.get_collection('notes')



