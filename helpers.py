import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup

class DBHelper:


    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name, check_same_thread=False)
        self.connect.row_factory=sqlite3.Row
        self.c=self.connect.cursor()


    def getRegion(self, region_id):
        return self.c.execute("select key_id,name from regions WHERE key_id=?", (region_id, )).fetchone()

    def getDataByTime(self, region_id, time):
        return self.c.execute("SELECT * FROM times WHERE region_id = ? and day= ?", (region_id, time)).fetchone()

    def regions(self):
        return self.c.execute("select name, key_id from regions").fetchall()

    def getTimes(self):
        self.driver = webdriver.Chrome("c:/Users/User/Downloads/chromedriver.exe")
        regions=self.regions()
        for region in regions:
            self.driver.get('https://islom.uz/vaqtlar/{}/5'.format(region['key_id']))
            content = self.driver.page_source
            soup = BeautifulSoup(content, "html.parser")
            for tr in soup.findAll('tr')[1:]:
                sahars.append(tr.contents[7].text)
                quyoshs.append(tr.contents[9].text)
                peshins.append(tr.contents[11].text)
                asrs.append(tr.contents[13].text)
                shoms.append(tr.contents[15].text)
                xuftons.append(tr.contents[17].text)
                days.append(tr.contents[3].text)
                self.c.execute(
                    "INSERT INTO times VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                        .format(tr.contents[7].text, tr.contents[9].text, tr.contents[11].text, tr.contents[13].text, tr.contents[15].text, tr.contents[17].text,
                                tr.contents[3].text, region['key_id']))
        self.connect.commit()

    def deleteAllTimes(self):
        self.c.execute("DELETE from times")
        self.connect.commit()

    def test(self):
        self.driver = webdriver.Chrome("c:/Users/User/Downloads/chromedriver.exe")
        self.driver.get('https://islom.uz/vaqtlar/13/5')
        content = self.driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        for tr in soup.findAll('tr')[1:]:
            print(tr.contents[3].text)
            print(tr.contents[7].text)
            print(tr.contents[9].text)
            print(tr.contents[11].text)
            print(tr.contents[13].text)
            print(tr.contents[15].text)
            print(tr.contents[17].text)

