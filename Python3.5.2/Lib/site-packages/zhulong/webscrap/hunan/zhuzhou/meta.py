import pandas as pd  
import re 

from selenium import webdriver 
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 


from  lmfscrap import web

#__conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]


# url="http://www.zzzyjy.cn/016/016001/1.html"
# driver=webdriver.Chrome()
# #driver.minimize_window()
# driver.get(url)


def f1(driver,num):
    locator=(By.CLASS_NAME,"ewb-info-list")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    cnum=int(re.findall("([0-9]{1,}).html",url)[0])
    locator=(By.XPATH,"//ul[@class='ewb-info-list']//li[1]//a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    val=driver.find_element_by_xpath("//ul[@class='ewb-info-list']//li[1]//a").text
    if cnum!=num:
        url=re.sub("[0-9]{1,}(?=.html)",str(num),url)
        driver.get(url)
        locator=(By.XPATH,"//ul[@class='ewb-info-list']//li[1]//a[string()!='%s']"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    page=driver.page_source
    soup=BeautifulSoup(page,'lxml')

    ul=soup.find("ul",class_="ewb-info-list")
    lis=ul.find_all("li",class_="ewb-list-node clearfix")
    data=[]
    for li in lis:
        a=li.find("a")
        span=li.find("span",recursive=False)
        tmp=[a["title"],"http://www.zzzyjy.cn"+a["href"],span.text.strip()]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df 


def f2(driver):
    locator=(By.CLASS_NAME,"ewb-info-list")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    if "下页" in driver.page_source:
        locator=(By.XPATH,"//ul[@class='ewb-info-list']//li[1]//a")
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

        total=int(driver.find_element_by_id("index").text.split("/")[1])
        driver.quit()
        return total
    else:
        driver.quit()
        return 1


def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":10



    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):

    data=[
        ["gcjs_fangwu_zhaobiao_gg","http://www.zzzyjy.cn/016/016001/016001001/1.html",["name","href","ggstart_time"]],

        ["gcjs_fangwu_zhongbiaohx_gg","http://www.zzzyjy.cn/016/016001/016001004/1.html",["name","href","ggstart_time"]],

        ["gcjs_fangwu_zhongbiao_gg","http://www.zzzyjy.cn/016/016001/016001006/1.html",["name","href","ggstart_time"]],


        ["gcjs_shizheng_zhaobiao_gg","http://www.zzzyjy.cn/016/016002/016002001/1.html",["name","href","ggstart_time"]],

         ["gcjs_shizheng_zhongbiaohx_gg","http://www.zzzyjy.cn/016/016002/016002004/1.html",["name","href","ggstart_time"]],

          ["gcjs_shizheng_zhongbiao_gg","http://www.zzzyjy.cn/016/016002/016002006/1.html",["name","href","ggstart_time"]],


        ["gcjs_jiaotong_zhaobiao_gg","http://www.zzzyjy.cn/016/016003/016003001/1.html",["name","href","ggstart_time"]],

         ["gcjs_jiaotong_zhongbiaohx_gg","http://www.zzzyjy.cn/016/016003/016003004/1.html",["name","href","ggstart_time"]],

          ["gcjs_jiaotong_zhongbiao_gg","http://www.zzzyjy.cn/016/016003/016003006/1.html",["name","href","ggstart_time"]],


        ["gcjs_shuili_zhaobiao_gg","http://www.zzzyjy.cn/016/016004/016004001/1.html",["name","href","ggstart_time"]],

         ["gcjs_shuili_zhongbiaohx_gg","http://www.zzzyjy.cn/016/016004/016004004/1.html",["name","href","ggstart_time"]],

          ["gcjs_shuili_zhongbiao_gg","http://www.zzzyjy.cn/016/016004/016004006/1.html",["name","href","ggstart_time"]],

          ["zfcg_zhaobiao_gg","http://www.zzzyjy.cn/017/017001/1.html",["name","href","ggstart_time"]],

            

            ["zfcg_zhongbiao_gg","http://www.zzzyjy.cn/017/017003/1.html",["name","href","ggstart_time"]],

            ["zfcg_biangen_gg","http://www.zzzyjy.cn/017/017002/1.html",["name","href","ggstart_time"]],

            ["zfcg_liubiao_gg","http://www.zzzyjy.cn/017/017004/1.html",["name","href","ggstart_time"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
        print(data)
    for w in data:
        general_template(w[0],w[1],w[2],conp)


conp=[]


