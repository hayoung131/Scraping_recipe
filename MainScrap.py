# -*- coding: utf-8 -*-
#i = filter(str.isdigit,s)
#print i
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
# import sys
# reload(sys)
import time
from urllib.request import Request, urlopen
import pymysql.cursors
import re

# import title
# import cook_info
import ingredient
# import cooking_step
import cooking_tip


base_url="http://www.10000recipe.com/recipe/list.html?order=accuracy&page={}"

# 레시피 링크가있는 돔 객체의 href를 뽑아내어 링크로 이루어진 list생성
def list_getter() :
    for k in range(len(li)) :
       # a=li[k].select("a").get_attribute('href')
        b = li[k].find("a")
        a="http://www.10000recipe.com"+b.get("href")


        linkList.append(a)

def scrapingRecipe():
    a_cooking_tip = cooking_tip.cooking_tip_scrap(bs)  # 요리 팁
    a_ingredient = ingredient.ingre_scrap(bs, bs, serving) #재료    

for i in range(100,102):
    linkList = list()
    i += 1  # 1
    print('현재 페이지 : ', i)
    url = base_url.format(i)
    re=Request(url)

    res1=urlopen(re)  # 첫 페이지 출력됨.
    bs1 = BeautifulSoup(res1, 'html.parser')
    # 레시피 리스트 돔객체 저장
    li = bs1.select(
        '#contents_area.col-xs-9 > div.rcp_m_list2 > div.row > div.col-xs-4')
    list_getter()  # li에 저장된 div들의 링크를 뽑아내는 작업
    print('현재 리스트 길이: ', len(linkList))
    print(linkList)
    for i in range(len(linkList)):

        req=Request(linkList[i])

        res=urlopen(req)
        bs = BeautifulSoup(res, 'html.parser')
        # if(checkRecipe() == 0):  # checkRecipe()의 리턴값이 0이면 크롤링안하고 continue.
        #     continue

        scrapingRecipe()

        print('     ',i+1, '번째 레시피')


