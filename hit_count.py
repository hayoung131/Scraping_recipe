# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
#import sys


#sys.setdefaultencoding('utf-8')

class hit_count_scrap:
    def __init__(self, soup):

        if(soup.select('#contents_area > div.view2_pic > div.view_cate.st2 > div > span')):
            self.hit_count = soup.select('#contents_area > div.view2_pic > div.view_cate.st2 > div > span')
            for i in range(len(self.hit_count)):
                self.hit_count = self.hit_count[i].text
                print("조회수 : ",self.hit_count)


    def hit_count_rt(self):
        return self.hit_count