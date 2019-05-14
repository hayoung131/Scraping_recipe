# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
#import sys


#sys.setdefaultencoding('utf-8')

class cooking_step_scrap :
    def __init__(self, driver):
        self.cooking_steps_list = list()

        self.num = driver.select('div.view_step > div > div.media-body')  # 조리과정 하나하나가 클래스명 media-body로 되어있음.
        for a in range(len(self.num)):
            # num1을 안에 또 선언할 필요없어서 지웠어!!
            # 그리고  cooking_steps = num[a].text 이렇게 하면 cooking_steps 의 내용이 전부 for문 돌때마다 리셋되버려서 cooking_steps 를 for문 밖에
            # scrapingRecipe()메소드 바로 아래에 , 리스트 형식으로 선언해둘게 그래야 맨마지막에 그 리스트내용을 문자열로 변환해서 디비에 저장할수 있음!!
            self.step = "step" + str(a + 1) + " : " + self.num[a].text
            self.cooking_steps_list.append(self.step)

       # cooking_steps_final = '\n'.join(self.cooking_steps_list)
        print('\n'.join(self.cooking_steps_list))  # cooking_steps 라는 리스트안에 있는 데이터들을 문자열로 출력하되, 계행하며 하나씩 출력하라는뜻!!
        # 그냥 print cooking_steps 라고 하니깐,, 유니코드 떠서 이렇게 해야할듯..!!

    def cooking_step_rt(self):
        return '\n'.join(self.cooking_steps_list)