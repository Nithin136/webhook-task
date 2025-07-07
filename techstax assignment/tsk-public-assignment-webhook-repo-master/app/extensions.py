import srv
from flask_pymongo import PyMongo, MongoClient

#Setup MongoDB here
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.0luyika.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
