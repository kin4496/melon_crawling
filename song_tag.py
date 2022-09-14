from typing import List, Union, Tuple
from bson.objectid import ObjectId

class SongTag:
    def __init__(self,tag:str,title:str,artist:Union[str,List[str]],song_id:ObjectId):
        self.tag=tag
        self.title=title
        if isinstance(artist,str):
            artist=[artist]
        self.artist=artist
        self.song_id=song_id

    def get_data(self):
        return {
            'tag':self.tag,
            'title':self.title,
            'artist':self.artist,
            'song_id':self.song_id
        }