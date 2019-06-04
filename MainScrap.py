# -*- coding: utf-8 -*-
#i = filter(str.isdigit,s)
#print i
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
# import sys
# reload(sys)
import time
import pymysql.cursors
import re
import title
import cook_info
import ingredient
import cooking_step
import cooking_tip
import hit_count


#sys.setdefaultencoding('utf-8')


#Chrome의 경우 아까 받은 chromedriver의 위치를 지정해준다.

# driver = webdriver.Chrome('C:\Chrome_Driver\chromedriver.exe') #driver는 그냥 웹저버의 객체이름임.
# driver.implicitly_wait(3) #암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.


# driver.get("http://www.10000recipe.com/recipe/6902125")
# time.sleep(1)
# webdriver.Chrome(path)는, 크롬드라이버로 크롬브라우저를 제어할 수 있는 창을 띄운다.
# 조금만 기다리면 selenium으로 제어할 수 있는 브라우저 새창이 뜬다
# 자동화된 테스트 소프트웨어에 의해 제어되고 있다는 말은 셀레니움으로 해당 브라우저를 제어할 수 있다는 말.
#
#pymysql.connect()메소드를 사용하여mysql에 connect 한다. 호스트명, 로그인, 암호, 접속할 DB 등을 파라미터로 지정한다.
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='111111',
                             db='recipedata',
                             # charset='utf-8'
                             )

# source = driver.page_source
# soup = BeautifulSoup(source, "html.parser")

base_url="http://www.10000recipe.com/recipe/list.html?order=accuracy&page={}"

def list_getter() :
    for k in range(len(li)) :
       # a=li[k].select("a").get_attribute('href')
        b = li[k].find("a")
        a="http://www.10000recipe.com"+b.get("href")


        linkList.append(a)


def checkRecipe():
    global replyNum
    global star_score_avg
    # contents_area > div.view_reply.st2
    #b = list()
    count = 0
    hit_check = hit_count.hit_count_scrap(bs)
    global hit_standard
    hit_standard = int(hit_check.hit_count_rt())  # 여기서도 조회수를 뽑아낸는 메소드를 호출함.


    # if soup.find("dl", {"class": "view_step_tip"}) :
    # <img src="http://recipe1.ezmember.co.kr/img/mobile/icon_star2_on.png">
    if (bs.select('#contents_area > div.view_reply.st2 > div.reply_tit')):  # 후기댓글이 있는경우!
        if (bs.find("div", {"class": "view_btn_more"})):  # 후기댓글 전체보기 버튼이 있다면
            replyMore1 = bs.select(
                '#contents_area > div.view_reply.st2 > div > div.media.reply_list')  # replyMore1 = 후기댓글 부분에 더보기 버튼을 누르지 않았을때 보이는 부분만을 가져옴!

            replyMore2 = bs.select('#moreViewReviewList > div.media.reply_list')  # replyMore2 = 더보기 버튼을 눌렀을때 나오는 후기댓글들을 가져옴!

            # star = soup.find_all("img")
            for star in bs.find_all("img"):  # img태그가 있는 부분을 모두 가져온다.
                if (star.get("src") == "http://recipe1.ezmember.co.kr/img/mobile/icon_star2_on.png"):   #  img태그 내용들중 각 이미지의 src부분이 노란색 별일때만 count++ 한다.
                    count = count + 1

            print ('전체보기버튼이 있습니다')
            print ('별 개수', count)#15
            replyNum = len(replyMore1) + len(replyMore2)  # 더보기 안눌렀을때 후기글 수 + 더보기 눌렀을때 후기글 수
            star_score_avg= round(float(count) / replyNum, 2)
            print ('레시피의 후기글 수 :', replyNum)#3
            print ('별점 평균 :', star_score_avg)


        else:  # 후기댓글 전체보기 버튼이 없다면
            reply = bs.select(
                '#contents_area > div.view_reply.st2 > div > div.media.reply_list')  # reply = 후기글 수.
            replyNum = len(reply)
            for star in bs.find_all("img"):
                if (star.get("src") == "http://recipe1.ezmember.co.kr/img/mobile/icon_star2_on.png"): #위의 노란 별 개수 세는것과 같은 코드.
                    count = count + 1

            star_score_avg = round(float(count) / replyNum, 2)
            print('전체보기 버튼이 없습니다.')
            print('별 개수', count)
            print('레시피의 후기글 수 :', replyNum)
            print('별점 평균 :', star_score_avg)

    if (hit_standard >= 1000):  #조회수가 1000 이상 일 때
        if (replyNum >= 1 or star_score_avg >= 4):  # 후기글 수가 1개보다 크고 별점이 4점이 넘으면 크롤링
            print('조회수가 1000이 넘습니다. 댓글도 있습니다.','댓글수 :', replyNum, '별점 평균 :', star_score_avg, '크롤링 합니다.')
            return 1  # 크롤링 할때는 1을 리턴하도록 한다.
        else:  #후기글 수가
            print('조회수가 1000이 넘지만 댓글은 없습니다.','댓글수 :', replyNum, '별점 평균 :', star_score_avg, '크롤링 합니다.')
            return 1
        # print('조회수가 1000이 넘습니다.','댓글수 :', replyNum, '별점 평균 :', star_score_avg, '크롤링 합니다.')
        # return 1
    else:
        if ( replyNum >= 1 or star_score_avg >= 4 ):
            print('크롤링 합니다.')
            return 1  # 1을 반환하면 크롤링
        else :
            print("크롤링 안하고 넘어갑니다.")
            return 0  # 0을 반환시켜 크롤링 안하게 함.



def scrapingRecipe(recipe_id):

    a_hit_count = hit_count.hit_count_scrap(bs)

    a_title = title.title_scrap(bs,bs) #제목
    #ttttitle = "임시 제목"

    a_cooking_info = cook_info.info_scrap(bs) #몇인분,시간,난이도

    serving = a_cooking_info.cooking_info_rt(0) #몇인분에 대한 정보를 변수에 넣음

    a_ingredient = ingredient.ingre_scrap(bs, bs, serving) #재료

    a_cooking_step = cooking_step.cooking_step_scrap(bs) #조리과정

    a_cooking_tip = cooking_tip.cooking_tip_scrap(bs) #요리 팁

    hit = int(a_hit_count.hit_count_rt())

    importance = replyNum*0.5 + (replyNum*0.3)*star_score_avg + hit*0.0005  #댓글 수 + 조회수 + 평점에 각각의 가중치를 곱하여 계산

    only_ingredient_name = a_ingredient.only_ingredient_name()
    ingredient_name_string = ",".join(only_ingredient_name)
    # print(a_ingredient.rt_dic_i())
    # print(a_ingredient.ingredient_dic.keys())
    # print(a_ingredient.ingredient_rt(1,2))
    # for cc in a_ingredient.ingredient_dic.keys():
    #     for dd in range(3):
    #         print(a_ingredient.ingredient_dic[cc][dd])
    # print(a_ingredient.ingredient_dic[0][0])
    # print(a_ingredient.ingredient_dic[0][1])
    # print(a_ingredient.ingredient_dic[0][2])


    #이거는 기본 레시피테이블에 넣을 것들


    cursor = connection.cursor()
        # Create a new record
    sql = "INSERT INTO mainrecipe(recipe_id,cooking_title, cooking_steps, cooking_tips, cooking_time, cooking_level,recipe_url,ingredient, ingredient_num,importance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (recipe_id, a_title.real_title_rt(), a_cooking_step.cooking_step_rt(), a_cooking_tip.cooking_tip_rt(), a_cooking_info.cooking_info_rt(1), a_cooking_info.cooking_info_rt(2),linkList[i], ingredient_name_string,len(only_ingredient_name),importance))

#     # db 접속이 성공하면, connection객체로부터 cursor()메소드를 호출하여 cursor 객체를 가져온다. db커서는 fetch동작을 관리하는데 사용하는데,
#     # 만약 db자체가 커서를 지원하지않으면, python db api에서 이 커서 동작을 emulation하게된다.
#     # Cursor 객체의 excute()메소드를 사용하여 SQL문장을 DB서버에 보낸다.
    ##############title 테이블에 삽입
    sql = "INSERT INTO title(recipe_id,title_id,searching_title) VALUES (%s,%s,%s)"
    cursor.execute(sql, (recipe_id, recipe_id, a_title.title_rt(bs)))

    ################comments 테이블에 삽입
    sql = "INSERT INTO comments(comments, star_score_avg,recipe_id,hit_standard) VALUES(%s,%s,%s,%s)"
    cursor.execute(sql, (replyNum, star_score_avg, recipe_id, hit_standard))


        ############################################이부분부터####################################################################
    for num in a_ingredient.ingredient_dic.keys():
            # Create a new record
        ####################재료 테이블에 삽입
        sql = "INSERT INTO recipe_ingredient(recipe_id,searching_ingredient,amount,measu) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, ( recipe_id, a_ingredient.ingredient_rt(num, 0),
                                 a_ingredient.ingredient_rt(num, 1),
                                 a_ingredient.ingredient_rt(num, 2)))  #자꾸 널 값으로 뜸,,,


        #     # db 접속이 성공하면, connection객체로부터 cursor()메소드를 호출하여 cursor 객체를 가져온다. db커서는 fetch동작을 관리하는데 사용하는데,
        #     # 만약 db자체가 커서를 지원하지않으면, python db api에서 이 커서 동작을 emulation하게된다.
        #     # Cursor 객체의 excute()메소드를 사용하여 SQL문장을 DB서버에 보낸다.
        #
    connection.commit()
#########################################3요기까지################################################################################################


#     connection.close()
cursor=connection.cursor()
sql="select count(*) from mainrecipe"
cursor.execute(sql) #매번 크롤링 할 때마다

cnt=cursor.fetchall()
recipe_id =cnt[0][0] # mainrecipe 테이블의 row 수를 반환할것. ((19,),)
print(recipe_id)

for i in range(1016,1100):
    replyNum = 0
    star_score_avg = 0.0
    linkList = list()
    i += 1  # 1
    print('현재 페이지 : ', i)
    url = base_url.format(i)
    re = Request(url)
    res1 = urlopen(re)  # 첫 페이지 출력됨.
    bs1 = BeautifulSoup(res1, 'html.parser')
    # 레시피 리스트 돔객체 저장
    li = bs1.select(
        '#contents_area.col-xs-9 > div.rcp_m_list2 > div.row > div.col-xs-4')
    list_getter()  # li에 저장된 div들의 링크를 뽑아내는 작업
    print('현재 리스트 길이: ', len(linkList))
    print(linkList)
    for i in range(len(linkList)):
        req = Request(linkList[i])
        time.sleep(1)
        res = urlopen(req)
        bs = BeautifulSoup(res,'html.parser')
        # source = driver.page_source
        # soup = BeautifulSoup(source, "html.parser")
        #scrapingPermit, star_score_avg2, replyNum2 =checkRecipe()
        if(checkRecipe() == 0):  # checkRecipe()의 리턴값이 0이면 크롤링안하고 continue.

            continue
        time.sleep(2)
        scrapingRecipe(recipe_id)

        recipe_id = recipe_id + 1
        print(i + 1, '번째 레시피')
        print('++++++++++++++++++++++++++++++++++++++++++++++')
connection.close()