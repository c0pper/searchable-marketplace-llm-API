import pymongo

# Replace these with your MongoDB connection details
mongo_uri = "mongodb+srv://dome-user:H3110_W0r1d@cluster0.0vfcpp8.mongodb.net/dome_demo?retryWrites=true&w=majority"

# Establish a connection to the MongoDB server
client = pymongo.MongoClient(mongo_uri)
db = client["dome_demo"]
collection = db["products"]
data = list(collection.find())