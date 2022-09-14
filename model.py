from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['music']
    return db

def get_collection(collection):
    db=get_db()
    return db[collection]

def get_song_tag_all(n_collection,tag):
    collection=get_collection(n_collection)
    return collection.find({'tag':tag})

def find_song_by_meta(n_collection,title,artist):
    if isinstance(artist,str):
        artist=[artist]
    collection=get_collection(n_collection)
    item=collection.find_one({
        'title':title,
        'artist':artist
    })
    return item

def find_song_by_id(n_collection,id):
    collection=get_collection(n_collection)
    item=collection.find_one({
        '_id':id
    })
    return item

def has_song_by_meta(n_collection,title,artist):
    item=find_song_by_meta(n_collection,title,artist)
    return item!=None

def has_song_by_id(n_collection,id):
    item=find_song_by_id(n_collection,id)
    return item!=None

def update_song_by_meta(n_collection,title,artist,id):
    if isinstance(artist,str):
        artist=[artist]
    collection=get_collection(n_collection)
    collection.update_many({'title':title,'artist':artist},{"$set":{"song_id":id}})
    
def save_data(n_collection,data):
    collection=get_collection(n_collection)
    return collection.insert_one(data).inserted_id


    
