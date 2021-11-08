from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.get_database('user')

food_list = db.get_collection('food_list')



