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

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver,num):


    locator=(By.ID,"index-list")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator=(By.XPATH,"//span[@class='pageBtnWrap']/span[@class='curr']")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    #cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    try:
        cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    except StaleElementReferenceException:
        cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    val=driver.find_element_by_xpath("//tbody[@id='index-list']/tr[2]/td[1]//a").text
    if num!=cnum:
        driver.execute_script("kkpager._clickHandler(%d)"%num)
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a[string()!='%s']"%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page=driver.page_source

    soup=BeautifulSoup(page,'lxml')

    tbody=soup.find("tbody",id="index-list")

    trs=tbody.find_all("tr")
    data=[]
    for tr in trs[1:]:
        a=tr.find("a")
        td=tr.find_all("td")[1]
        tmp=[a["title"],td.text.strip(), "https://ggzy.changsha.gov.cn"+a["href"]]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df 

def cp(f):
    return f

def f2(driver):
    locator=(By.XPATH,"//span[@class='totalPageNum']")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    try:
        total=driver.find_element_by_xpath("//span[@class='totalPageNum']").text
    except StaleElementReferenceException:
        total=driver.find_element_by_xpath("//span[@class='totalPageNum']").text
    total=int(total)
    driver.quit()
    return total

def zhongbiao_gg(f):
    def wrap(*krg):
        driver=krg[0]
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val=driver.find_element_by_xpath("//tbody[@id='index-list']/tr[2]/td[1]//a").text
        locator=(By.ID,"index-list")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath("//ul[@id='trade-list-item']/li[@data-val='RESULT_NOTICE'][@style='display: list-item;']").click()
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a[string()!='%s']"%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def qita_gg(f):
    def wrap(*krg):
        driver=krg[0]
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val=driver.find_element_by_xpath("//tbody[@id='index-list']/tr[2]/td[1]//a").text
        locator=(By.ID,"index-list")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        locator=(By.XPATH,"//ul[@id='trade-list-item']/li[@data-val='WEB_JY_NOTICE']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath("//ul[@id='trade-list-item']/li[@data-val='WEB_JY_NOTICE'][@style='display: list-item;']").click()
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a[string()!='%s']"%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def zhongbiaohx_gg(f):
    def wrap(*krg):
        driver=krg[0]
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val=driver.find_element_by_xpath("//tbody[@id='index-list']/tr[2]/td[1]//a").text
        locator=(By.ID,"index-list")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath("//ul[@id='trade-list-item']/li[@data-val='PUBLICITY'][@style='display: list-item;']").click()
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a[string()!='%s']"%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def kongzhijia_gg(f):
    def wrap(*krg):
        driver=krg[0]
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val=driver.find_element_by_xpath("//tbody[@id='index-list']/tr[2]/td[1]//a").text
        locator=(By.ID,"index-list")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath("//ul[@id='trade-list-item']/li[@data-val='92'][@style='display: list-item;']").click()
        locator=(By.XPATH,"//tbody[@id='index-list']/tr[2]/td[1]//a[string()!='%s']"%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def general_template(tb,url,col,f,conp):

    m=web()
    setting={
    "url":url,
    "f1":f(f1),
    "f2":f(f2),
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":10,


    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):
    data=[
    ["gcjs_fangwushizheng_zhaobiao_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type11",["name","ggstart_time","href"],cp],

    ["gcjs_fangwushizheng_zhongbiaohx_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type1",["name","ggstart_time","href"],zhongbiaohx_gg ],

    ["gcjs_fangwushizheng_qita_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type1",["name","ggstart_time","href"],qita_gg ],

    ["gcjs_fangwushizheng_kongzhijia_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type1",["name","ggstart_time","href"],kongzhijia_gg ],


    ["gcjs_jiaotong_zhaobiao_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2",["name","ggstart_time","href"],cp],

    ["gcjs_jiaotong_zhongbiaohx_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2",["name","ggstart_time","href"],zhongbiaohx_gg ],

    ["gcjs_jiaotong_qita_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2",["name","ggstart_time","href"],qita_gg ],

    ["gcjs_jiaotong_kongzhijia_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2",["name","ggstart_time","href"],kongzhijia_gg ],




    ["gcjs_shuili_zhaobiao_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type3",["name","ggstart_time","href"],cp],

    ["gcjs_shuili_zhongbiaohx_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type3",["name","ggstart_time","href"],zhongbiaohx_gg ],

    ["gcjs_shuili_qita_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type3",["name","ggstart_time","href"],qita_gg ],

    ["gcjs_shuili_kongzhijia_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type3",["name","ggstart_time","href"],kongzhijia_gg ],



    ["zfcg_zhaobiao_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type4",["name","ggstart_time","href"],cp],

    ["zfcg_zhongbiao_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type4",["name","ggstart_time","href"],zhongbiao_gg ],

    ["zfcg_qita_gg","https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type4",["name","ggstart_time","href"],qita_gg ],




        
    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],w[3],conp)
