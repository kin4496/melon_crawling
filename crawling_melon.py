import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from song_tag import SongTag
from song_meta import Song

#song_tag,song_meta를 가져올 때 공통적으로 쓰는 함수들
def wait(start,end):
    t=random.randint(start,end)
    time.sleep(t)

def get_driver():
    options=Options()
    prefs={'profile.default_content_setting_values':{
        'cookies':2,
        'images':2
    }}
    options.add_experimental_option('prefs',prefs)
    options.add_argument('--disable-extensions')

    driver = webdriver.Chrome(options=options)
    return driver

def clean_cmd(cmd):
    if cmd.startswith('javascript:'):
            cmd=cmd.removeprefix('javascript:')
    return cmd

def find_element(parent,by,filter):
    elements=parent.find_elements(by,filter)
    if len(elements)==0:
        return None
    else:
        return elements[0]

def find_elements(parent,by,filter):
    return parent.find_elements(by,filter)

#song_tag를 크롤링할 때 쓰는 함수들
def get_song_tag_from_melon(driver,tag,page=1,isDebug=False):
    #url로 이동
    url = 'https://www.melon.com/dj/themegenre/djthemegenre_list.htm'
    driver.get(url)

    #태그 입력
    tag_input=find_element(driver,By.ID,'djSearchKeyword')
    if tag_input==None:
        print('태그 입력창을 찾지 못했습니다.')
        return None
    tag_input.send_keys(tag)

    #검색 버튼 클릭
    search_btn=find_element(driver,By.XPATH,'//*[@id="conts"]/div[1]/div[2]/div[2]/button')
    if search_btn==None:
        print('검색 버튼을 찾지 못했습니다.')
        return None
    search_btn.click()
    
    #플레이리스트 이동하는 cmd 가져오기
    playListCmd=get_playlist_cmd(driver,page)

    song_tags=[]
    #플레이리스트에 담긴 노래 정보 가져오기
    for cmd in playListCmd:
        song_tags+=get_song_tag_from_playlist(driver,tag,cmd)

        #디버그용이라면 첫번째 플레이리스트만 가져와서 반환하기
        if isDebug:
            return song_tags

    return song_tags

def get_playlist_cmd(driver,page):
    
    #플레이리스트 가져오기
    playLists=find_elements(driver,By.CLASS_NAME,"album_name")
    
    #href 속성 가져오기
    playLists=list(map(lambda x:x.get_attribute('href'),playLists))
    
    #cmd에 있는 javascript: 삭제
    playLists=list(map(clean_cmd,playLists))

    return playLists

def get_song_tag_from_playlist(driver,tag,cmd):
   
    #플레이리스트 페이지로 이동
    driver.execute_script(cmd)
    wait(1,2)

    #제목 정보가 있는 태그 가져오기
    titles=find_elements(driver,By.CLASS_NAME,'rank01')
    #제목 정보가 있는 a 태그 가져오기
    titles=list(map(lambda x:find_element(x,By.TAG_NAME,'a'),titles))
    #제목만 가져오기
    titles=list(map(lambda x:x.get_attribute('title'),titles))
    titles=list(map(lambda x:x.removesuffix(' 재생'),titles))

    #가수 정보가 있는 태그 가져오기
    artists=find_elements(driver,By.CLASS_NAME,'rank02')
    #가수 정보가 있는 a 태그 가져오기
    artists=list(map(lambda x:find_element(x,By.TAG_NAME,'a'),artists))

    #가수만 가져오기
    artists=list(map(lambda x:x.get_attribute('title') if x != None else '',artists))
    artists=list(map(lambda x:x.removesuffix(' - 페이지 이동'),artists))
    artists=list(map(lambda x:x.split(','),artists))

    song_tags=[]

    #song_tag 리스트 생성후 반환
    for title,artist in zip(titles,artists):
        song_tags.append(SongTag(tag=tag,title=title,artist=artist,song_id=None))
    
    return song_tags

#song_meta에서 가사 크롤링할 때 쓰는 함수
def get_song_meta_from_melon(driver,song_tag):

    #현재 멜론 홈페이지에 있지 않다면 이동
    url='https://www.melon.com/'
    if driver.current_url != url:
        driver.get(url)
    
    #아이피 벤을 막기 위해서 20초에서 30초가량 기다리기
    wait(20,30)

    #노래 제목과 가수명
    title=song_tag.title
    artist=song_tag.artist

    #검색 바 찾아서 검색하기
    search_bar=find_element(driver,By.ID,'top_search')
    if search_bar==None:
        print('검색 창을 찾을 수 없습니다.')
        return None
    search_bar.send_keys(artist[0]+' '+title)

    #검색 버튼 눌러 검색하기
    search_btn=find_element(driver,By.XPATH,'//*[@id="gnb"]/fieldset/button[2]')
    if search_btn==None:
        print('검색 버튼을 찾을 수 없습니다.')
        return None
    search_btn.click()
    wait(1,2)

    #가사 정보 페이지로 이동
    lyric_btn=find_element(driver,By.XPATH,'//*[@id="frm_songList"]/div/table/tbody/tr[1]/td[3]/div/div/a[1]')
    if lyric_btn==None:
        print('가사 정보를 찾을 수 없습니다.')
        return None
    lyric_btn.click()
    wait(1,2)

    #가사 가져오기
    lyric=find_element(driver,By.ID,'d_video_summary')
    if lyric!=None:
        lyric=lyric.text
    
    #발매일 가져오기
    issue_date=find_element(driver,By.XPATH,'//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[2]')
    if issue_date != None:
        issue_date=issue_date.text
    
    #장르 가져오기
    genre=find_element(driver,By.XPATH,'//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]')
    if genre != None:
        genre=genre.text
    
    return Song(title=title,artist=artist,issue_date=issue_date,genre=genre,lyric=lyric)

if __name__=="__main__":
    driver=get_driver()
    url= 'https://www.melon.com/dj/themegenre/djthemegenre_list.htm'

    song_tags=get_song_tag_from_melon(driver,'사랑',isDebug=True)
    print(song_tags[0].title)

    song_meta=get_song_meta_from_melon(driver,SongTag('벚꽃','벚꽃엔딩','버스커버스커',None))
    print(song_meta.lyric)
