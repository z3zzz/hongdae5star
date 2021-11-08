from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.get_database('user')

user_info = db.get_collection('user_info')
email_list = db.get_collection('email_list')



