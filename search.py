# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 13:26:41 2022

@author: 고종민
"""

import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from konlpy.tag import Okt
from nltk import Text


import time

#import pymongo  # version - 2.8.1
import getpass

def get_tickers():
    url = "https://api.upbit.com/v1/market/all"
    headers = {"accept":"application/json"}
    response = requests.get(url, headers=headers)
    data=response.json()
    #print(response.text)
    #print(type(data))
    tickers=[]
    for market in data:
        #print(type(market))
        tickers.append(market['korean_name'])
    return tickers

okt = Okt()
def get_crawl(timing):
    timing.clear()
    old_coin=[]
    top_coin=[]
    buy_target=[]
    old_wordInfo=dict()

    #url = "https://api.upbit.com/v1/market/all?isDetails=false"

    #headersa = {"Accept": "application/json"}

    #response = requests.request("GET", url, headers=headersa)
    #atx=response
    
    atx=str(get_tickers())

# URL 
    #f = open('writ.csv','a', newline='')
    #wr = csv.writer(f) 
    BASE_URL = "https://gall.dcinside.com/board/lists/?id=bitcoins_new1&page=" 
    Domain_URL = "https://gall.dcinside.com" 
# 헤더 설정
    content_list=""
    headers=[ {'User-Agent' : 'grapeshot'}, ] 
 # html 
    counting=[]
    for ban in range(0,2):
        #time.sleep(3)
        try:
            #time.sleep(0.5)
            buy_target=[]
            for k in range(9-8*(ban),16-8*(ban)):
                #time.sleep(10)
                try:
                    #response = requests.get(BASE_URL+str(k), headers=headers[0],timeout=5) 
                    response = requests.get(BASE_URL+str(k), headers=headers[0],timeout=5) 
                    soup = BeautifulSoup(response.content, 'html.parser') 
                    html_list = soup.find('tbody').find_all('tr') 
                except:
                    return 0
                for i in html_list: 
                    try:
                        title_list = i.find('a', href=True).text
                    except:
                        title_list = "오류 게시글"
# 주소 
                    #try:
                        #date_tag = i.find('td', class_='gall_date').text
                    #except:
                        #date_tag=today
            #gall_list = i.find('strong') 
#갤러리이름 # 
        #a=a+"조회수"
                    a=title_list.find("삼성")
        #print(a)
                    b=title_list.find("무료")
                    c=content_list.find(title_list)
                    if a ==-1 and b==-1 and c==-1:
                        content_list = content_list + title_list
                        time.sleep(0.01)
            #print(title_list,date_tag,count)
            #z=date_tag.find(":")
            #o=date_tag.find("/")
                    #time.sleep(2)
            myList = okt.pos(content_list, norm=True, stem=True) # 모든 형태소 추출
            myList_filter = [x for x, y in myList if y in ['Noun']] # 추출된 값 중 동사만 추출
            #myList_filterA=[a for a in myList_filter if a in ['구조대','지옥','불장','대장','횡보','도망','운지','폭락','반등','자살','물장','롱충','숏충','매수','매도','저점','고점']]
            Okt = Text(myList_filter, name="Okt")
            wordInfo = dict()
            for tags, counts in Okt.vocab().most_common(40):
                if(len(str(tags)) > 1):
                    wordInfo[tags] = counts
            values = sorted(wordInfo.values(), reverse=True)
            keys = sorted(wordInfo, key=wordInfo.get, reverse=True)
            #df=pd.DataFrame(keys,index=values,columns=['빈도'])
            #k=np.array(keys,values)
            m=[]
        #counting+=[wordInfo["매수"]]
        #print(counting)
        #print("매수",wordInfo["매수"])
            cnt=0
            for i in range(0,len(keys)):
                m+=[[keys[i],values[i]]]
                if (keys[i]=="매수" or keys[i]=="쏜다" or keys[i]=="반등" or keys[i]=="가자" or keys[i]== "불장" or keys[i]=="찐반"):
                    cnt+=int(values[i])
                #print(cnt)
            counting+=[cnt]
        #print(counting)
            #print(keys[i],values[i],ban)
        #print(m)
            #npy=np.array(m)
        #print(npy)
        #for sen in m:
            #print(sen[1])
            for i in keys:
                bea=atx.find(i)
                if bea!=-1:
                    top_coin+=[i]
                #print("사야할거",top_coin)
                #print(top_coin)
        #print(top_coin)
            for coin in top_coin:
        #mm=top_coin.find(coin)
                if (coin in old_coin) != 1:
                    buy_target+=[coin]
                #print(buy_target,"이 새로 생겨남",l)
                try:
                    if int(old_wordInfo[coin])>=int(wordInfo[coin])*3:
                        buy_target+=[coin]
                    #print([coin],"이 더 비싸질거라 구매")
                except:
                #print("not found")
                    pass
                    time.sleep(0.05)
                    #print("error")
            old_wordInfo=wordInfo.items()
    #keys=[]
    #values=[]
            content_list=""
            old_coin=top_coin
            top_coin=[]
        #print(str(buy_target)+"를 구매")
        except:
            print("error")
            return "error"
            #pass
    if int(counting[1])<=int(counting[0]):
        #print(counting[1]-counting[0])
        timing+=["a"]
    else:
        timing+=["b"]
    #timing+=["b"]
        #print(amen)
    #print(counting)
    #print(timing)
    return(buy_target)
#amen=[]
#print(get_crawl(amen))
#print(amen)
#if "a" in amen:
    #print("매수타이밍")
#else:
    #print("매도타이밍")
#print(get_crawl(amen))
#print(amen)

