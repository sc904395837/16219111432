# -*-coding:utf-8 -*-
import io
import sys
#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import requests
import MySQLdb
from lxml import etree

def get_page(start_num):
    url = 'https://movie.douban.com/top250?start=%s&filter='%start_num
    res = requests.get(url)

    tree = etree.HTML(res.text)
    top250 = tree.xpath('//span[@class="title"][1]/text()')
    print(top250)
    return top250

top250 = get_page(0)
print(top250)

def get_all_page(start,end):
    result = []
    for i in range(start,end-start):
        title_list = get_page(i*25)
        result += title_list

    return result



topMovies = []
topMovies= get_all_page(0,10)
url = 'https://movie.douban.com/top250?start=%s&filter='
conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='world',charset='utf8')
cur = conn.cursor()
for i in topMovies:
    cur.execute("INSERT INTO testmodle_test(id,content) VALUES(%s, %s)",(id,str(i)))


    

cur.close()
conn.commit()
conn.close()
