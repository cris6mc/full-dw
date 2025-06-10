from pymongo import MongoClient

# conexion local
# db_client = MongoClient().local

# conexion remota
db_client = MongoClient("mongodb+srv://cris6mc:zIsuQ42aUrpQXcgf@cluster0.xhxyejg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

