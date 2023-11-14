import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27037/")
mydb = myclient["admin"]
mycol = mydb["Awards"]

x = mycol.find_one()

print(x)