import model
from song_tag import SongTag
n_collection='topic'
song_tags=model.get_song_tag_all(n_collection,'이별')

for song_tag in song_tags:
    song_tag=SongTag(tag=song_tag['tag'],title=song_tag['title'],artist=song_tag['artist'],song_id=song_tag['song_id'])
    
    title=song_tag.title
    artist=song_tag.artist
    song_id=song_tag.song_id
    item=model.find_song_by_meta('song_meta',title,artist)
    if item!=None:
        id=item['_id']
        song_tag.song_id=id
        model.update_song_by_meta(n_collection,title,artist,id)