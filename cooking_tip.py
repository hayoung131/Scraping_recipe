# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
#import sys


#sys.setdefaultencoding('utf-8')

class cooking_tip_scrap:
    def __init__(self, soup):
        if (soup.find("dl", {"class": "view_step_tip"})):
            self.cooking_tip = soup.find("dl", {"class": "view_step_tip"}).text
            print ('***************tip**************', self.cooking_tip, '**************tip***************')
        else :
            self.cooking_tip = "No tip"

        print ('=' * 20)

    def cooking_tip_rt(self):
        return self.cooking_tip
    