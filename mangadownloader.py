import urllib
from urllib.request import urlopen, Request 
import requests
from PIL import Image
import io
import os
import re
import time


url2 =  "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-1/01.jpg"
base_url =  "https://www.scan-vf.co/uploads/manga/one_piece/chapters"

#req = urllib.request.Request(url2, headers={'User-Agent' : "Magic Browser"}) 
#con = urllib.request.urlopen( req )
#f = io.BytesIO(con.read())
#byteImg = Image.open(f)
#byteImg.save('test.jpg', 'JPEG')

def test():
    fwcURL = "https://www.scan-vf.co/one_piece/chapitre-2" #URL to read
    req = urllib.request.Request(fwcURL,  headers={'User-Agent' : "Magic Browser"})
    mylines = urllib.request.urlopen(req).readlines()
    print("Found URLs:")
    match = re.findall(r'https://ww[w4].scan-vf.com?/uploads/manga/([^\'" >]+)', str(mylines))
    print(match)
    #for line in mylines:
        #print(line)
        #time.sleep(1) #Pause execution for a bit
        #links = re.findall('"((http|ftp)s?://.*?)"', str(line))  
        #match = re.findall(r'href=[\'"]?([^\'" >]+)', str(line))
        #print (match)
    for i in match:
        print(i)

def load_chapter(manga_name, chap_nbr):
    fwcURL = "https://www.scan-vf.co/" + manga_name + "/chapitre-" + str(chap_nbr) #URL to read
    req = urllib.request.Request(fwcURL,  headers={'User-Agent' : "Magic Browser"})
    mylines = urllib.request.urlopen(req).readlines()
    print("Found URLs:")
    match = re.findall(r'data-src=\\[\']?\s([^\'" >]+)', str(mylines))
    for page in range(len(match)):
        req = urllib.request.Request(match[page],  headers={'User-Agent' : "Magic Browser"})
        con = urllib.request.urlopen(req)
        f = io.BytesIO(con.read())
        byteImg = Image.open(f)
        byteImg.save(os.path.expanduser("~/Documents/" + manga_name + "/chapter-" + str(chap_nbr) + "/" + '%02d' % (page + 1)  + ".jpg"), 'JPEG')
        print("page number " + '%02d' % (page + 1))
    print()



def folder_manager(manga_name, chapter):
    url = "https://www.scan-vf.co/uploads/manga/" + manga_name + "/chapters"
    done = 1
    chap_nbr = 1
    if not(os.path.isdir(os.path.expanduser("~/Documents/" + manga_name))):
        os.mkdir(os.path.expanduser("~/Documents/" + manga_name))
    while done <= chapter:
        if not(os.path.isdir(os.path.expanduser("~/Documents/" + manga_name + "/chapter-" + str(done)))):
            print("Downloading Chapter " + str(done) + "\n")
            os.mkdir(os.path.expanduser("~/Documents/" + manga_name + "/chapter-" + str(done)))
            load_chapter(manga_name, done)
        else :
            print("Chapter already downloaded" + str(done) + "\n")
        done += 1
    print("finished chapters \n")


def manga_dl():
    manga_name = input("enter manger name (with spaces) : ")
    print(manga_name)

    try:
        req = urllib.urlopen("https://www.scan-vf.co/one_piece/chapitre-1") 
        print("it exist")
    except:
        print("nope")

folder_manager("one_piece", 250)


