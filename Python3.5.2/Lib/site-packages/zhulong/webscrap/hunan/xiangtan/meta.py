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

# __conp=["postgres","since2015","192.168.3.171","hunan","xiangtan"]


# url="https://ggzy.xiangtan.gov.cn/zbgg/index_1.jhtml"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver,num):
    locator=(By.CLASS_NAME,"text-list")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    cnum=int(re.findall("index_([0-9]{1,}).jhtml",url)[0])
    locator=(By.XPATH,"//div[@class='text-list']/ul/li[2]//a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    val=driver.find_element_by_xpath("//div[@class='text-list']/ul/li[2]//a").text
    if cnum!=num:
        url=re.sub("(?<=index_)[0-9]{1,}(?=.jhtml)",str(num),url)
        driver.get(url)
        locator=(By.XPATH,"//div[@class='text-list']/ul/li[2]//a[string()!='%s']"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


    page=driver.page_source
    soup=BeautifulSoup(page,'lxml')

    ul=soup.find("div",class_="text-list")

    lis=ul.find_all("li",class_="tabletitle tabletitle2")
    data=[]
    for li in lis:
        a=li.find("a")
        em=li.find("em")
        tmp=[a["title"],a.text,"https://ggzy.xiangtan.gov.cn"+a["href"],em.text.strip()]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df 

def f2(driver):

    locator=(By.CLASS_NAME,"text-list")
    WebDriverWait(driver,20).until(EC.presence_of_element_located(locator))

    locator=(By.XPATH,"//div[@class='text-list']/ul/li[2]//a")
    WebDriverWait(driver,20).until(EC.presence_of_element_located(locator))

    info=driver.find_element_by_xpath("//div[@class='pagesite']").text
    total=re.findall("记录[\s0-9]{1,2}/([0-9]{1,})页",info)[0]
    total=int(total)
    driver.quit()
    return total

def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":10,


    }
    m=web()
    m.write(**setting)

def work(conp,i=-1):
    data=[
        ["gcjs_zhaobiao_gg","https://ggzy.xiangtan.gov.cn/zbgg/index_1.jhtml",["name","title","href","ggstart_time"]],

       ["gcjs_zhongbiaohx_gg","https://ggzy.xiangtan.gov.cn/zbhxrgs/index_1.jhtml",["name","title","href","ggstart_time"]],

          ["gcjs_qita_gg","https://ggzy.xiangtan.gov.cn/zsjggs/index_1.jhtml",["name","title","href","ggstart_time"]],

            ["zfcg_zhaobiao_gg","https://ggzy.xiangtan.gov.cn/cggg/index_1.jhtml",["name","title","href","ggstart_time"]],

            ["zfcg_biangen_gg","http://ggzy.xiangtan.gov.cn/gzgg/index_1.jhtml",["name","title","href","ggstart_time"]],

            ["zfcg_qita_gg","https://ggzy.xiangtan.gov.cn/ygg/index_1.jhtml",["name","title","href","ggstart_time"]],

            ["zfcg_zhongbiao_gg","https://ggzy.xiangtan.gov.cn/jggg/index_1.jhtml",["name","title","href","ggstart_time"]],
    ]

    if i==-1:
        data=data
    else:
        data=data[i:i+1]

    for w in data:
        general_template(w[0],w[1],w[2],conp)
