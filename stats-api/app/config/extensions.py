from pymongo import MongoClient
from flask import current_app



def init_mongo(app):
    host = app.config["MONGODB_HOST"]
    port = app.config["MONGODB_PORT"]
    user = app.config.get("MONGODB_USERNAME")
    pwd  = app.config.get("MONGODB_PASSWORD")

    if user and pwd:
        client = MongoClient(
            host=host,
            port=port,
            username=user,
            password=pwd,
            authSource="admin",
        )
    else:
        client = MongoClient(host=host, port=port)

    app.extensions["mongo_client"] = client
    
    try:
        client.admin.command('ping')
        app.logger.info(f"Connected to MongoDB: {app.config['MONGODB_HOST']}")
    except Exception as e:
        app.logger.error(f"Error while connecting to MongoDB: {e}")
        raise

def get_mongo_client():
    return current_app.extensions['mongo_client']

def get_db():
    if 'mongo_client' not in current_app.extensions:
        raise RuntimeError("MongoDB hasn't be initialized")
    
    client = current_app.extensions['mongo_client']
    db_name = current_app.config['MONGODB_DATABASE']
    return client[db_name]


def get_collection(collection_name=None):
    db = get_db()
    collection_name = collection_name or current_app.config['MONGODB_COLLECTION']
    return db[collection_name]