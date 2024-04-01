import os
from bs4 import BeautifulSoup
import requests

from datetime import datetime
import pywintypes

import time
import zipfile
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sys




options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(options=options)



url = "https://cafe.naver.com/flashfriend/"
clubid = 28351014
menuid = 64
pageNum = 1
userDisplay = 15


driver.get(url + 'ArticleList.nhn?search.clubid=' + str(clubid) + '&search.menuid=' + str(menuid) +'&search.page='+ str(pageNum) +'&userDisplay=' + str(userDisplay))

driver.switch_to.frame('cafe_main')



soup = BeautifulSoup(driver.page_source, 'html.parser')

soup = soup.find_all(class_ = 'article-board m-tcol-c')
soup = soup[1]


datas = soup.find_all(class_ = 'td_article')

gdrvFnd=0
sliced=''
UGdate = 0 #updated game date
UGmonth =''
UGday =''

while(gdrvFnd==0):
    for data in datas:
        article_title = data.find(class_ = 'article')
        link = article_title.get('href')
        opened = requests.get(url+link)
        openedHTML = opened.text
        soup = BeautifulSoup(openedHTML, 'html.parser')
        finded = openedHTML.find("drive.google.com")
        sliced = openedHTML[finded:finded+300]
        sliced = sliced[sliced.find("file/d")+7:sliced.find("view")-1]
        if finded!=-1:
            UGdate = soup.find(class_="date").get_text()
            if UGdate[5] == 0:
                UGmonth = int(UGdate[6])
            else:
                UGmonth = int(UGdate[5:7])
            if UGdate[8] == 0:
                UGday = int(UGdate[9])
            else:
                UGday = int(UGdate[8:10])
            gdrvFnd = 1
            break
    if finded == -1:
        print("알 수 없는 오류로 업데이트를 찾을 수 없습니다.")
        os.system("pause")
        exit()




year = datetime.today().year


drvURL = 'https://drive.usercontent.google.com/download?id='+sliced+'&export=download'

driver.get(drvURL)

DrvSoup = BeautifulSoup(driver.page_source, 'html.parser')
DrvLoc = DrvSoup.find(id='download-form')
final = 'https://drive.usercontent.google.com/download?id='+sliced+'&export=download&confirm=t&uuid='+DrvLoc.find_all("input")[4]["value"]


driver.quit()



#final = "https://drive.usercontent.google.com/download?id=1_rpHIVwy4eh5ErmgaBVwN6l67zIUwOLZ&export=download&confirm=t&uuid=a5db59ac-6efb-4f6a-a6a6-da9547ff9f5d"


def download():
    
    from urllib.request import urlretrieve

    urlretrieve(final, "./Dead_Dota.zip")
    while 1:
        a = input("파일을 압축 해제하려면 y를 해제하지 않고 끝내려면 n을 누르세요 : ")

        if a == "y":
            Dead_dota_zip = zipfile.ZipFile('./Dead_Dota.zip')
            Dead_dota_zip.extractall('./')
            Dead_dota_zip.close()

            while 1:
                b = input("원본 압축 파일을 삭제하시곘습니까? y/n: ")
                if b == "y":
                    os.remove("./Dead_Dota.zip")
                    break
                else:
                    os.system("pause")
                    exit()
                    break
        else:
            os.system("pause")
            exit()
            break
            
        os.system("pause")
        exit()



file_name = ""
f = ""
fdata = ""



def file_find():
    try:
        global file_name
        file_name = "dead_dota.exe"
        
        f = open( "./"+file_name , 'rb')
        fdata = f.read()
        f.close()
    except:
        while 1:
            a = input("dead_dota.exe 가 존재하지 않습니다. 그냥 최신버전을 다운로드하겠습니까? y/n : ")
            if a == "y":
                download()
            
file_find()


fltime = time.ctime(os.path.getmtime( file_name ))
flmonth = fltime[4:7]
fltimeslicing = fltime[fltime.find(flmonth)+5:]
flday = int(fltimeslicing[0:fltimeslicing.find(" ")])

if flmonth == "Oct":
    flmonth = 10
if flmonth == "Jan" or flmonth == "jan":
    flmonth = 1
if flmonth == "Fab" or flmonth == "fab":
    flmonth = 2
if flmonth == "Mar" or flmonth == "mar":
    flmonth = 3
if flmonth == "Apr" or flmonth == "apr":
    flmonth = 4
if flmonth == "May" or flmonth == "may":
    flmonth = 5
if flmonth == "Jun" or flmonth == "jun":
    flmonth = 6
if flmonth == "Jul" or flmonth == "jul":
    flmonth = 7
if flmonth == "Aug" or flmonth == "aug":
    flmouth = 8
if flmonth == "Sep" or flmonth == "fab":
    flmonth = 9
if flmonth == "Nov" or flmonth == "nov":
    flmonth = 11
if flmonth == "Dec" or flmonth == "dec":
    flmonth = 12


if UGmonth <= flmonth:
    if UGday <= flday:
        print("버전이 최신 버전입니다!")
    else:
        print("새로운 버전이 있습니다. 다운로드를 진행합니다.")
        download()
else:
    print("새로운 버전이 있습니다. 다운로드를 진행합니다.")
    download()
