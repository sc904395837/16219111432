#coding:utf-8
from selenium import webdriver
import os
import time
import pymysql.cursors

class Crawler(object):
    def __init__(self):
        self.Chromedriver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = self.Chromedriver
        self.Chrome = webdriver.Chrome(self.Chromedriver)

        # Connect to the database
        self.MySql = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456',
                                     db='world',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

    def crawling36kr(self):
        url = "https://www.36kr.com/information/web_news"
        # 添加cookie前必须先打开一次网站
        self.Chrome.get(url)
        cookie = { "name" : "new_user_guidance", "value" : "true", "domain" : ".36kr.com"}
        self.Chrome.add_cookie(cookie)
        self.Chrome.get(url)
        time.sleep(3)

        item_list = self.Chrome.find_elements_by_class_name("kr-shadow-content")
        print("item_list = ", len(item_list))
        index = 0
        while index < len(item_list) - 1:
            item = item_list[index]
            index += 1
            item.location_once_scrolled_into_view
            imgSrc = item.find_element_by_class_name("scaleBig").get_attribute("src")
            title = item.find_element_by_class_name("article-item-title")
            path = title.get_attribute("href")
            print(index, " len = ", len(item_list), " img = " , imgSrc , " path = " , path, " title = ", title.text)

            self.news_detail_36kr(index, item)
            item_list = self.Chrome.find_elements_by_class_name("kr-shadow-content")
            time.sleep(2)
            
            if index == len(item_list) - 1:
                loading_more_button = self.Chrome.find_element_by_class_name("kr-loading-more-button")
                loading_more_button.location_once_scrolled_into_view
                time.sleep(3)
                item_list = self.Chrome.find_elements_by_class_name("kr-shadow-content")
                if index == len(item_list) - 1:
                    loading_more_button.click()
                    time.sleep(3)
                    item_list = self.Chrome.find_elements_by_class_name("kr-shadow-content")
                

    def news_detail_36kr(self, index, item):
        imgSrc = item.find_element_by_class_name("scaleBig").get_attribute("src")
        title = item.find_element_by_class_name("article-item-title")
        path = title.get_attribute("href")

        title.click()
        # select second page
        num = self.Chrome.window_handles
        self.Chrome.switch_to_window(num[1])
        time.sleep(5)
        # get content
        article_title = self.Chrome.find_element_by_class_name("article-title")
        author = self.Chrome.find_element_by_class_name("title-icon-item")
        summary = self.Chrome.find_element_by_class_name("summary")
        p_list = self.Chrome.find_elements_by_xpath("//*[@id='app']/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/p")
        print("article_title == ", article_title.text, " author = ", author.text, " summary = ", summary.text, " len(p_list) = ", len(p_list))
        content = ""
        for p in p_list:
            content += p.text
            print(content)

        # insert Data to db
        # try:
        try:
            with self.MySql.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `testmodle_dontai` (`title`, `url`, `img`, `author`, `summary`, `content`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (article_title.text, path, imgSrc, author.text, summary.text, content))
            # connection is not autocommit by default. So you must commit to save your changes.
            self.MySql.commit()
        except Exception as e:
            print(e)

        time.sleep(3)
        self.Chrome.close()
        self.Chrome.switch_to_window(num[0])
            
if __name__ == "__main__":
     crawler = Crawler()
     crawler.crawling36kr() 
