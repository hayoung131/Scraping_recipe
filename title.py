# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import sys
#reload(sys)
import time
import pymysql.cursors
import urllib3.request #형태소분석 api는 웹으로 제공하는 서비스이기에 이게 필요함.
import requests#형태소분석 api는 웹으로 제공하는 서비스이기에 이게 필요함.
import numpy as np  # 행렬 라이브러리 numpy
import re

secret_key="6011420040561756864"
morp_url="http://api.adams.ai/datamixiApi/tms?query="
option="&lang=kor&analysis=pos&key="


class title_scrap:
    def __init__(self, driver, soup):
        # driver=webdriver.Chrome('D:/Downloads/chromedriver.exe')
        # driver.implicitly_wait(3)
        # driver.get("http://www.10000recipe.com/recipe/6909745")
        # time.sleep(1)
        # source=driver.page_source
        # soup=BeautifulSoup(source, "html.parser")


        ##전역변수 선언
        final_foodName_list=[]


        def morp(text) :
            noun_text = ""
            query = text # 이거 뭐가 특수문자 이런거 있으면 아예 안들어가지는 것 같음......ㅠ

            url_query = morp_url + query + option + secret_key
            #검색 요청을위해 쿼리 문자열을 입력인자로 Request개체를 생성하기
            #request=urllib3.request.Request(url_query)
            response = requests.get(url=url_query)


            #print response.text
            #print type(response.text)
            #print len(response.text)
            #print response.text[0]
            #print(response.url)
            # for i in range(len(response.text)):
            #     string_tag = string_tag + response.text[i]
            string_tag = "".join(response.text)
            print ('이거 아무것도 안나옴' , string_tag ,response.text)

            try:
                #print eval(string_tag)
                dict_tag = eval(string_tag) #딕셔너리형식으로된 문자열을 딕셔너리로 형전환.
                for j in range(len(dict_tag['return_object']['sentence'])):
                    for i in range(len(dict_tag['return_object']['sentence'][j]['morp'])):
                        if(dict_tag['return_object']['sentence'][j]['morp'][i]['type'] == 'NNG' or dict_tag['return_object']['sentence'][j]['morp'][i]['type']=='NNP'):
                            noun_text=noun_text+dict_tag['return_object']['sentence'][j]['morp'][i]['lemma']+' '
            except SyntaxError:
                string_tag = '얘는 딕셔너리로 바꿀 수 없습니다.'
                print (string_tag)
            return noun_text

        def title_similarity(title, sent):
            words1 = title.split()  # 제목이 공백 구분자로 나눠서 list 로 드가있음.
            words2 = sent.split()
            total = words1 + words2  # (제목+sent2를 모두 담은 벡터 생성)
            total_vocab = list(set(total))  # 공통 부분 없애려고 그러는거군...
            vocab_size = len(total_vocab)
        # []
            title_vec = np.zeros(vocab_size)  # numpy.zeros(n)은 길이가 n인 0으로 채워진 벡터를 만든다. numpy.ones(n)은 1로 채워진 벡터.
            sentense_vec = np.zeros(vocab_size)
            for i in range(vocab_size):
                if words1.count(total_vocab[i]) > 0:
                    title_vec[i] = 1
                if words2.count(total_vocab[i]) > 0:
                    sentense_vec[i] = 1
            a=' '.join(total_vocab) #토탈 단어 리스트를 담은 리스트가 유니코드로 나와서 이케 함..
            print ('제목+문장       : ', a)
            print ('제목 백터       : ', title_vec)
            print ('sents 백터     : ', sentense_vec)
            food_name=[] #
            for i in range(vocab_size):
                if title_vec[i]==sentense_vec[i] :
                    food_name.append(total_vocab[i])
            print ('#중간 음식명    : ',' '.join(food_name))
            print ("_____________________________________________")
            return food_name

        #제목 크롤링  ##########################################이 위치에 있어야함.
        title_sents = soup.find("h3").text
        Noun_title_sents = morp(title_sents)
        self.real_title = soup.find("h3").text


        #태그 크롤링#

        if (soup.find("div", {"class": "view_tag"})) : ###########################################################이거 추가해써###############################################
            food_tag = soup.find("div", {"class": "view_tag"}).text
            food_tag=food_tag.split('#') #리스트 형식에 들어감

            del food_tag[0]# #을 기준으로 나누다보니... 첫번째에는 공백이 들어가거든. 그래서 지워야함.
            food_tag= ' '.join(food_tag)
            self.Noun_food_tag = food_tag
            li_t = title_similarity(Noun_title_sents,self.Noun_food_tag) #############################return value = 요리명 list
            final_foodName_list.extend(li_t) #최종음식이름 리스트에 저 리스트를 합치기


        #추천 태그 크롤링
        recommand_tag_crawling = soup.find("ul",{"class":"view_pdt_recipe2"}).find_all("a",{"class":"tag"})
        if (recommand_tag_crawling):
            recommand_tag=""
            for i in range(len(recommand_tag_crawling)) :
                recommand_tag=recommand_tag+recommand_tag_crawling[i].get_text() + ''
            recommand_tag=recommand_tag.split('#')
            del recommand_tag[0]
            recommand_tag=' '.join(recommand_tag)
            print (recommand_tag)
            print ('추천태그 타입이 뭐니',type(recommand_tag))
            Noun_recommand_tag=recommand_tag
            li_rt=title_similarity(Noun_title_sents, Noun_recommand_tag)
            final_foodName_list.extend(li_rt)


        #추천레시피 제목 크롤링
        recommend_recipes = driver.select('div.caption.jq_elips2')  # 추천 레시피 제목 추출
        sents = list() # 추천레시피 제목 들어갈 리스트 변수

        for i in range(4):
            sents.append(recommend_recipes[i].text)
        sents = ' '.join(sents)
        print ('추천레시피 ',sents)
        print (type(sents))

        s = sents
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')# 한글과 띄어쓰기를 제외한 모든 글자
        # hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')  # 위와 동일
        dddd = hangul.sub('', s) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
        print ('엿같네..',dddd)
        Noun_recommand_recipes = morp(dddd)
        li_rr = title_similarity(Noun_title_sents, Noun_recommand_recipes)
        final_foodName_list.extend(li_rr)



        #이부분이 빈도수 체크하는부분
        # def word_count(text):
        #
        #     wordAll = text.split(' ') #공백을 기준으로
        #     wordDic = {}
        #     print wordAll
        #     print type(wordAll)
        #     for i in wordAll:
        #         wordCnt = wordAll.count(i)
        #         wordDic[i] = wordCnt #각각 단어를 key로 하고 빈도수는 value에 삽입.
        #     print("\n당신이 입력하신 문장의 단어수는 아래와 같습니다.\n")
        #
        #     for cnts in wordDic:
        #         print cnts, wordDic[cnts]

        print ('제목(명사만)       :  ',Noun_title_sents)
        if (soup.find("div", {"class": "view_tag"})) :
            print ('태그(명사만)       :  ',self.Noun_food_tag)
        print ('추천태그(명사만)    :  ',Noun_recommand_tag)
        print ('추천레시피(명사만)  :  ',Noun_recommand_recipes)

        print ('____________최종 추출된 음식명____________________')
        #print ' '.join(final_foodName_list)
        print (' '.join(set(final_foodName_list))) #중복 제거
        self.final_title = ' '.join(set(final_foodName_list));

    def title_rt(self,soup):#전처리한 제목+태그 합친것 보내기
        if(soup.find("div", {"class": "view_tag"})):
            return self.Noun_food_tag+self.final_title
        else:
            print("태그없음. 전처리제목만 보내겠음")
            return self.final_title
    def real_title_rt(self): #전처리하지않은 제목
        return self.real_title
    # def tag_rt(self,soup):
    #     if (soup.find("div", {"class": "view_tag"})):
    #         return self.Noun_food_tag
    #     else:
    #         return "No tag"
