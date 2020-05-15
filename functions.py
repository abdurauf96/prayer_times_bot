from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3


conn = sqlite3.connect('ramadan.sqlite', check_same_thread=False)
c=conn.cursor()

class getRegions:

    region_id=18
    sahars = []
    quyoshs = []
    peshins = []
    asrs = []
    shoms = []
    xuftons = []
    days=[]

    driver = webdriver.Chrome("c:/Users/User/Downloads/chromedriver.exe")
    driver.get('https://islom.uz/vaqtlar/18/5')
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    for tr in soup.findAll('tr')[1:]:
        sahars.append(tr.contents[7].text)
        quyoshs.append(tr.contents[9].text)
        peshins.append(tr.contents[11].text)
        asrs.append(tr.contents[11].text)
        shoms.append(tr.contents[13].text)
        xuftons.append(tr.contents[15].text)
        days.append(tr.contents[3].text)

    for sahar,quyosh,peshin,asr,shom,xufton,day in zip(sahars,quyoshs,peshins,asrs,shoms,xuftons,days):
        c.execute("INSERT INTO times VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(sahar,quyosh,peshin,asr,shom,xufton,day,region_id))
    conn.commit()