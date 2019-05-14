# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
#import sys
import re


#sys.setdefaultencoding('utf-8')

class ingre_scrap:
    def __init__(self, soup, driver, a):
        # a가 a_cooking_info.cooking_info_rt() 이거인 셈.
        # 변수 선언
        self.aa = list()
        self.ingredient = list()
        self.amount_measure = list()


        # 뷰티풀 숲 사용하기위한 단계
        self.ingredient_dic = {}  # 이거슨 딕셔너리 선언할때 쓰는거


        if (soup.find("div", {"id": "divConfirmedMaterialArea"})):
            # 만약 이 id를 가진 태그가 존재한다면 이부분을 실행
            self.cooking_ingredients = driver.select('#divConfirmedMaterialArea > ul.case1 > li')

            for i in range(len(self.cooking_ingredients)):
                self.final_ingredient = [0, 0, 0]
                # cooking_ingredients[i].text.rstrip()
                self.aa.append(self.cooking_ingredients[i].text)
                # print i + 1, '번째 재료', aa[i]  # ***********이거 안됨 개빡침
                # print " ".join(aa[i].split())
                
    def rt_dic_i(self):
        return len(self.ingredient_dic)

    def ingredient_rt(self, i, j):

        return self.ingredient_dic[i][j] #딕셔너리 안에서 몇번째값의 몇번째 번지를 가져올지 정하는거
