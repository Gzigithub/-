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

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
def general_template(tb,url,col,conp):

    m=web()
    setting={
    "url":url,
    "f1":f1,
    "f2":f2,
    "tb":tb,
    "col":col,
    "conp":conp,
    "num":5,


    }
    m=web()
    m.write(**setting)


def f1(driver,num):
    locator=(By.XPATH,"//div[@class='contentText']/ul/li/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    if "index.html" in url:
        cnum=1
    else:
        cnum=int(re.findall("index_([0-9]{1,}).html",url)[0])+1
    if num!=cnum:
        if num==1:
            url=re.sub("index[_0-9]*.html","index.html",url)
        else:
            s="index_%d.html"%(num-1) if num>1 else "index.html"
            url=re.sub("index[_0-9]*.html",s,url)
        val=driver.find_element_by_xpath("//div[@class='contentText']/ul/li[1]/a").text 
        driver.get(url)

        locator=(By.XPATH,"//div[@class='contentText']/ul/li[1]/a[not(contains(string(),'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))


    page=driver.page_source

    soup=BeautifulSoup(page,"lxml")

    div=soup.find("div",class_="contentText")

    lis=div.find_all("li",class_="nyLine")

    data=[]

    for li in lis:
        a=li.find("a")
        span=li.find("span")
        tmp=[a.text.strip(),span.text.strip(),a["href"]]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    return df 


def f2(driver):
    if "clsPage" in driver.page_source:

        locator=(By.XPATH,"//div[@class='clsPage']//a[contains(string(),'尾页')]")
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

        href=driver.find_element_by_xpath("//div[@class='clsPage']//a[contains(string(),'尾页')]").get_attribute("href")
        if "index.html" in href:
            total=1
        else:

            total=int(re.findall("index_([0-9]{1,}).html",href)[0])+1

        driver.quit()
        return total
    else:
        return 1

def work(conp,i=-1):
    data=[

        ["gcjs_zhaobiao_gg","http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html",["name","ggstart_time","href"]],

        ["gcjs_zhongbiaohx_gg","http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbhxrgs_64798/index.html",["name","ggstart_time","href"]],


        ["gcjs_qita_gg","http://ggzy.hengyang.gov.cn/jyxx/jsgc/qtgg_64799/index.html",["name","ggstart_time","href"]],


        ["zfcg_zhaobiao_gg","http://ggzy.hengyang.gov.cn/jyxx/zfcg/zbgg_64800/index.html",["name","ggstart_time","href"]],

        ["zfcg_zhongbiao_gg","http://ggzy.hengyang.gov.cn/jyxx/zfcg/jggs/index.html",["name","ggstart_time","href"]],


        ["zfcg_qita_gg","http://ggzy.hengyang.gov.cn/jyxx/zfcg/qtgg_64802/index.html",["name","ggstart_time","href"]],


    ]
    if i==-1:
        data=data
    else:
        data=data[i:i+1]
    for w in data:
        general_template(w[0],w[1],w[2],conp)
