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
                temp1 = " ".join(self.aa[i].split()).split()
                self.ingredient.append(temp1[0])  # temp1(0)는 재료들 감자 소금 등등.. 넣는 리스트 채썬 표고 다시마 멸치,,
                self.amount_measure.append(temp1[1])  # temp1(1)은 1kg 20개 등등
                self.final_ingredient[0] = self.ingredient[i]

                # print temp1
                # print " ".join(ingredient)
                # print amount_measure

                ######## 이제 여기서부터 숫자랑 단위 분리하는 작업.   ########
                s = str("".join(self.amount_measure[i]))  # str은 밑에 한글 인식을 해야하기 때문에 문자열로 바꿔둠 그냥 놔두면 ex4513321이렇게 이상하게 나옴
                # print s, '이게 현재 s에 들어있는 값임'
                # re.compile(검색할 문자열) : 이 함수는 정규식 패턴을 입력으로 받아들여 정규식 객체를 리턴함. (re.RegexObject 클래스 객체)
                detach = re.compile('[a-zA-Z]+|[ㄱ-ㅣ가-힣]+')  # 영어와 한글제외한 (숫자)뽑아내기
                # 영어 [a-zA-Z]+
                # 한글 [ㄱ-ㅣ가-힣]+
                amount = detach.sub('', s)  # 한글과 띄어쓰기를 제외한 모든 부분을 제거 //숫자만 나오게
                measu = ''.join(detach.findall(s))  # 정규식에 일치되는 부분을 리스트 형태로 저장 //숫자제외 나머지
                self.final_ingredient[2] = measu
                # print (num)
                if amount == '':  # 한글로만 되어있을 경우 약간 조금 등등
                    self.final_ingredient[1] = '0'  # 0l 이라는 문자를 넣는다.
                # measu = ''.join(detach.findall(s))  # 정규식에 일치되는 부분을 리스트 형태로 저장 //숫자제외 나머지
                # self.final_ingredient[2] = measu

                else:  # 이게 숫자도 같이 있는거 1/4, 30 등등
                    just_num = float(
                        ''.join(re.findall("\d+", a)))  # 4인분에서 숫자부분만뽑아내서 float형으로 바꿈

                    try:                                      #타입에러가 났을 경우 예외 처리함.
                        amount = float(eval(amount))   # num은 1/4 같은 계산식도 섞여있을수 있기때매 eval을 써서 자체적으로 계산을 처리한 후 float형으로 바꿈
                        math = amount / just_num  # 재료 양 / 인분 지금 amount에서 int값만 있으면 에러남..?
                        math = round(math, 2)  # 위의 결과값에서 소수점 2자리까지만 나오게 함

                        if math <= 0.0:
                            self.final_ingredient[1] = '0'
                            self.final_ingredient[2] = '소량'
                        else:
                            self.final_ingredient[1] = math
                            measu = ''.join(detach.findall(s))
                            self.final_ingredient[2] = measu
                    except TypeError:
                            self.final_ingredient[1] = '123456'
                            self.final_ingredient[2] = 'Type Error'

                        # print final_ingredient[1], '제발!!!!!!!!!!!!!1'


                         # print ''.join(measu)

                        #print final_ingredient, '이거는 각 재료들끼리 리스트!!'


                    self.ingredient_dic[i] = self.final_ingredient

                    print (i + 1, "번째 재료 :   ", self.final_ingredient[0], self.final_ingredient[1], self.final_ingredient[2])
                    #print i
                    print(self.ingredient_dic)  # 이게 딕셔너리!!
                    #print ''.join(self.ingredient_dic[0][0]) #이거는 각 딕셔너리안의 리스트로 된 값의 첫번째가 뽑아지는지 확인한것..!

                
    def rt_dic_i(self):
        return len(self.ingredient_dic)

    def ingredient_rt(self, i, j):

        return self.ingredient_dic[i][j] #딕셔너리 안에서 몇번째값의 몇번째 번지를 가져올지 정하는거
