from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import urllib.request
import sqlite3
# -*-coding:utf-8 -*-
import io
import sys
#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import requests
import MySQLdb
from lxml import etree
'''
url = "http://www.weather.com.cn/weather/101300101.shtml"
try:
    headers = {"User-Agent":"Mozilla/5.0(Windows;U;Windows NT 6.0 x64;en-US;rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
    req = urllib.request.Request(url,headers=headers)
    data = urllib.request.urlopen(req)
    data = data.read()
    dammit = UnicodeDammit(data,["utf-8","gbk"])
    data = dammit.unicode_markup
    soup = BeautifulSoup(data,"lxml")
    lis = soup.select("ul[class='t clearfix'] li")
    for li in lis:
        try:
            date = li.select('h1')[0].text
            weather = li.select('p[class="wea"]')[0].text
            temp = li.select('p[class="tem"] span')[0].text + "/" + li.select('p[class="tem"] i')[0].text
            print(date,weather,temp)
        except Exception as err:
            print(err)
except Exception as err:
    print(err)
'''
def insert(city,date,weather,temp):
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='world',charset='utf8')
        cur = conn.cursor()
        cur.execute("INSERT INTO testmodle_weathers(City,Date,weather,Teap) VALUES(%s,%s,%s,%s)",(city,date,weather,temp))
        cur.close()
        conn.commit()
        conn.close()
    except Exception as err:
        print(err)




class WeatherForecast:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0(Windows;U;Windows NT 6.0 x64;en-US;rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
        self.cityCode = {"北京":"101010100","南宁":"101300101","上海":"101020100","广州":"101280101"}

    def forecastCity(self,city):
        if city not in self.cityCode.keys():
            print (city+"code cannot be found")
            return

        url="http://www.weather.com.cn/weather/"+self.cityCode[city]+".shtml"
        try:
            req = urllib.request.Request(url,headers=self.headers)
            data = urllib.request.urlopen(req)
            data = data.read()
            dammit = UnicodeDammit(data,["utf-8","gbk"])
            data = dammit.unicode_markup
            soup = BeautifulSoup(data,"lxml")
            lis = soup.select("ul[class='t clearfix'] li")
            n=0
            for li in lis:
                try:
                    date = li.select('h1')[0].text
                    weather = li.select('p[class="wea"]')[0].text
                    if n>0:
                        temp = li.select('p[class="tem"] span')[0].text + "/" + li.select('p[class="tem"] i')[0].text
                    else:
                        temp = li.select('p[class="tem"] i')[0].text 
                    print(city,date,weather,temp)
                    insert(city,date,weather,temp)
                    n=n+1
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)


    def process(self,cities):
        for city in cities:
            self.forecastCity(city)

ws = WeatherForecast()
ws.process(["北京","南宁","上海","广州"])