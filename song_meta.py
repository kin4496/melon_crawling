from typing import List, Union, Tuple

class Song:
    def __init__(self,title:str,artist:Union[str,List[str]],issue_date:str,genre:str,lyric:str):
        self.title=title
        self.artist=artist
        self.issue_date=issue_date
        self.genre=genre
        self.lyric=lyric
    
    def has_lyric(self):
        return self.lyric!=None
    
    def get_data(self):
        return {
            'title':self.title,
            'artist':self.artist,
            'issue_date':self.issue_date,
            'genre':self.genre,
            'lyric':self.lyric
        }
    
    def get_year(self):
        if self.issue_date==None:
            return None
        info=self.issue_date.split('.')
        if len(info)<1:
            return None
        return info[0]
    
    def get_month(self):
        if self.issue_date==None:
            return None
        info=self.issue_date.split('.')
        if len(info)<2:
            return None
        return info[1]
    
    def get_day(self):
        if self.issue_date==None:
            return None
        info=self.issue_date.split('.')
        if len(info)<3:
            return None
        return info[2]
    