import argparse
from tqdm import tqdm
import copy

import crawling_melon as melon
import model

from song_meta import Song
from song_tag import SongTag

if __name__=="__main__":

    #추출할 태그 인자값으로 설정
    parser = argparse.ArgumentParser("")
    parser.add_argument('tag',nargs='+')
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument('--alone',action='store_true')
    parser.add_argument('-c')
    args=parser.parse_args()

    #인자 값 가져오기
    tags=args.tag
    page=args.page
    n_collection=args.c
    if n_collection == None:
        print('collection 이름이 없습니다.')
        exit()
    alone=args.alone
    
    song_tags=[]

    #멜론에서 특정 태그 노래 가져오기
    driver=melon.get_driver()
    for tag in tags:
        diff_tags=copy.deepcopy(tags)
        diff_tags.remove(tag)
        song_tags+=melon.get_song_tag_from_melon(driver,tag,alone=alone,page=page,diff_tags=diff_tags)
    
    #태그 노래 데이터베이스에 저장
    for song_tag in song_tags:

        title=song_tag.title
        artist=song_tag.artist

        #이미 가사정보를 가지고 있는지 확인하고 있다면 song_id에 저장
        item=model.find_song_by_meta('song_meta',title,artist)
        if item!=None:
            id=item['_id']
            song_tag.song_id=id
        
        #데이터 베이스에 이미 저장되어있다면 데이터 베이스에 저장하지 않는다.
        if model.has_song_by_meta(n_collection,title,artist):
            continue
        
        model.save_data(n_collection=n_collection,data=song_tag.get_data())
    
    print('데이터 베이스에 '+' '.join(tags)+'를 포함하는 노래 리스트를 저장했습니다.')

    song_tags=[]
    

    #데이터 베이스에 들어있는 노래 리스트 가져오기
    for tag in tags:
        song_tags+=model.get_song_tag_all(n_collection,tag)
    
    print('멜론에서 노래 가사,발매일,장르 크롤링을 시작합니다.')

    #멜론에서 노래 가사,발매일,장르 크롤링한 후 데이터베이스에 저장
    for song_tag in tqdm(song_tags):
        
        song_tag=SongTag(tag=song_tag['tag'],title=song_tag['title'],artist=song_tag['artist'],song_id=song_tag['song_id'])

        title=song_tag.title
        artist=song_tag.artist
        song_id=song_tag.song_id

        # song_meta 컬렉션에 이미 저장되어있으면 크롤링하지 않는다.
        if song_id != None or model.has_song_by_meta('song_meta',title,artist):
            continue
        
        song_meta=melon.get_song_meta_from_melon(driver,song_tag)

        #노래 정보를 크롤링하지 못하면 저장하지 않는다.
        if song_meta == None:
            continue
        
        #크롤링된 정보와 함께 데이터베이스에 저장
        id=model.save_data('song_meta',song_meta.get_data())

        #n_collection에 song_id값 저장
        model.update_song_by_meta(n_collection,title=song_meta.title,artist=song_meta.artist,id=id)
    
    print('작업을 완료했습니다.')

    

    




        
    


