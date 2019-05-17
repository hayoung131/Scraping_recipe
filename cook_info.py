# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
#import sys


#sys.setdefaultencoding('utf-8')

class info_scrap :
    def __init__(self, driver):
        self.cooking_info = list()  # 몇인분, 조리시간, 난이도를 담을 리스트

        info = ['몇인분?', '조리시간', '난이도']  # 프린트 위해서

        for a in range(3):  # range(2)하니까 난이도가 출력이안되더라. 바꿨어

            self.infoScraping = driver.select(
                '#contents_area > div.view2_summary > div.view2_summary_info > span')  # 3가지 한번에 있는 태그,배열로 저장되어있음

            self.cooking_info.append(self.infoScraping[a].text)  # 몇인분, 조리시간, 난이도 순서로 배열에 대입

            print ('#', info[a], self.cooking_info[a])

    def cooking_info_rt(self, i):
        return self.cooking_info[i]

