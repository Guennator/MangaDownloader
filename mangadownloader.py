import urllib
from urllib.request import urlopen, Request 
import requests
from PIL import Image
import io
import os
import re


url2 =  "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-1/01.jpg"
base_url =  "https://www.scan-vf.co/uploads/manga/one_piece/chapters"

#req = urllib.request.Request(url2, headers={'User-Agent' : "Magic Browser"}) 
#con = urllib.request.urlopen( req )
#f = io.BytesIO(con.read())
#byteImg = Image.open(f)
#byteImg.save('test.jpg', 'JPEG')

def fetch_url_data(url):
    #print("fetching image url ")
    try :
        req = urllib.request.Request(url,  headers={'User-Agent' : "Magic Browser"})
        return urllib.request.urlopen(req)
    except:
        print("error 502 reloading page")
        return fetch_url_data(url)

def fetch_url(url):
    try :
        req = urllib.request.Request(url,  headers={'User-Agent' : "Magic Browser"})
        return urllib.request.urlopen(req).readlines()
    except:
        print("error 502 reloading chapter")
        return fetch_url_data(url)

def load_chapter(manga_name, chap_url, chap_nbr):
    fwcURL = "https://www.scan-vf.co/" + manga_name + chap_url #URL to read
    mylines = fetch_url(fwcURL)
    print("Found URLs:")
    match = re.findall(r'data-src=\\[\']?\s([^\'" >]+)', str(mylines))
    match_len = len(match)
    for page in range(match_len):
        con = fetch_url_data(match[page])
        f = io.BytesIO(con.read())
        byteImg = Image.open(f)
        end = match[page][-3:]
        if end == "png" :
            byteImg.save(os.path.expanduser("~/Documents/MangaDownloader/" + manga_name + "/chapter-" + str(chap_nbr) + "/" + '%02d' % (page + 1)  + ".png"), 'PNG')
            print("page number " + '%02d' % (page + 1) + ".png")
        else:
            byteImg.save(os.path.expanduser("~/Documents/MangaDownloader/" + manga_name + "/chapter-" + str(chap_nbr) + "/" + '%02d' % (page + 1)  + ".jpg"), "JPEG")
            print("page number " + '%02d' % (page + 1) + ".jpg")
    print()

def find_chapter(manga_name):
    fwcURL = "https://www.scan-vf.co/" + manga_name #URL to read
    mylines = fetch_url(fwcURL)
    match = re.findall(r'href=[\'"]?' + fwcURL + '([^\'" >]+)', str(mylines))
    return match
    

def folder_manager(manga_name, chapter):
    if not(os.path.isdir(os.path.expanduser("~/Documents/MangaDownloader/" + manga_name))):
        os.mkdir(os.path.expanduser("~/Documents/MangaDownloader/" + manga_name))
    chapters_links = find_chapter(manga_name)
    print("chapters Urls: " + str(len(chapters_links)) + " founded")
    chapter_rank = 1
    if chapter == 0:
        chapter = len(chapters_links)
    for i in range (len(chapters_links) - 1,len(chapters_links) - chapter - 1 ,-1):
        if not(os.path.isdir(os.path.expanduser("~/Documents/MangaDownloader/" + manga_name + "/chapter-" + str(chapter_rank)))):
            print("downloading chapter - " + '%02d' % chapter_rank + " / " + str(chapter - chapter_rank) +" left to download\n")
            os.mkdir(os.path.expanduser("~/Documents/MangaDownloader/" + manga_name + "/chapter-" + str(chapter_rank)))
            load_chapter(manga_name, chapters_links[i], chapter_rank)
        else:
            print("chapter - " + '%02d' % (chapter_rank) + " already downloaded / " + str(chapter - i - 1) +"left to download\n")
        chapter_rank += 1
        


def manga_dl():
    manga_name = input("enter manger name (with spaces) : ")
    print(manga_name)

    try:
        req = urllib.urlopen("https://www.scan-vf.co/one_piece/chapitre-1") 
        print("it exist")
    except:
        print("nope")

folder_manager("one_piece",0)



