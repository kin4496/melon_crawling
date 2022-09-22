from pymongo import MongoClient
import pandas as pd
import os

def get_db(n_db='music'):
    client = MongoClient("mongodb://localhost:27017/")
    db = client[n_db]
    return db
db=get_db()

def get_collection(collection):
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



def get_dataFrame():
    
    titles=[]
    artists=[]
    lyrics=[]
    issue_dates=[]
    moods=[]
    sits=[]
    topics=[]
    genres=[]
    
    song_metas=get_collection('song_meta').find()
    
    n_collections=db.list_collection_names()
    
    for song_meta in song_metas:
        
        id =song_meta['_id']
        title=song_meta['title']
        lyric= song_meta['lyric']
        artist= song_meta['artist']
        issue_date = song_meta['issue_date']
        genre = song_meta['genre']
        
        titles.append(title)
        lyrics.append(lyric)
        artists.append(artist)
        issue_dates.append(issue_date)
        genres.append(genre)
        
        topics.append(None)
        moods.append(None)
        sits.append(None)
        
        for n_collection in n_collections:
            
            if n_collection == 'song_meta':
                continue
            collection = db[n_collection]
            item=collection.find_one({
                'song_id':id
            })
            
            tag = item['tag'] if item != None else None
            
            if n_collection == 'topic':
                topics[-1]=tag
            elif n_collection == 'mood':
                moods[-1]=tag
            elif n_collection == 'situation':
                sits[-1]=tag
    return pd.DataFrame({'title':titles,'artist':artists,'lyric':lyrics,'genre':genres,'issue_date':issue_dates,'topic':topics,'mood':moods,'situation':sits})
                
def get_excel(path='./',fname='train.xlsx'):
    df=get_dataFrame()
    df.to_excel(os.path.join(path,fname))

def get_csv(path='./',fname='train.csv'):
    df=get_dataFrame()
    df.to_csv(os.path.join(path,fname))

def get_json(path='./',fname='train.json'):
    df=get_dataFrame()
    df.to_json(os.path.join(path,fname))
