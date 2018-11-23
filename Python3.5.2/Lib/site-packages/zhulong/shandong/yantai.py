import time

import pandas as pd
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs

from collections import OrderedDict


_name_='yantai'
def f1(driver,num):
    df=f1_1(driver,num)
    df["ggstart_time"]=df[df.columns[2]].map(lambda x:x.split("至")[0].strip() if len(x.split("至"))==2 else '' )
    df["ggend_time"]=df[df.columns[2]].map(lambda x:x.split("至")[1].strip() if len(x.split("至"))==2 else '')
    df["info"]=None
    for i in range(len(df)):
        df.at[i,"info"]=json.dumps({"ggend_time":df.at[i,"ggend_time"],"diqu":df.iat[i,0]},ensure_ascii=False)
    del df[df.columns[2]]
    return df 


def f1_1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, "(//div[@class='article-list3-t'])[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url

    page_1 = 58
    if "channelId=264" in url:
        locator = (By.XPATH, '(//ul[@class="pages-list"]/li)[1]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page_1 = re.findall('/(\d+)', page_all)[0]
    page_2 = int(page_1)
    if ("channelId=264"in url) or ("channelId=265" in url):

        df = f1_data(driver, num, url, page_2)
        return df
    # print(url)

    else:
        cnum = int(re.findall("queryContent_(.*)-", url)[0])
        if num != cnum:
            if num == 1:
                url = re.sub("queryContent_[0-9]*-", "queryContent_1-", url)
            else:
                s = "queryContent_%d-" % (num) if num > 1 else "queryContent_1-"
                url = re.sub("queryContent_[0-9]*-", s, url)
                # print(cnum)
            val = driver.find_element_by_xpath('(//ul[@class="pages-list"]/li)[1]').text
            # print(url)
            driver.get(url)
            # time.sleep(1)
            # print("1111")
            locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        ul = soup.find("ul", class_="article-list2")
        trs = ul.find_all("li")
        data = []
        for li in trs:
            try:
                info_number = li.find("span", class_="blue-w").text
                info = re.findall(r"\[(.*)\]", info_number)[0]
            except:
                info = ""
            a = li.find("a")
            title = a["title"]
            link = a["href"]
            try:
                date = li.find("div", class_="list-times").text
            except:
                date = li.find("p", class_="bmZhong").text

            tmp = [info.strip(), title.strip(), date.strip(), link.strip()]
            data.append(tmp)
        df = pd.DataFrame(data=data)
        return df


def f1_data(driver, num, url, page_1):
    cnum = int(re.findall("queryContent_(.*)-", url)[0])
    if num != cnum:
        if num <= page_1:
            if num == 1:
                url = re.sub("queryContent_[0-9]*-", "queryContent_1-", url)
            else:
                s = "queryContent_%d-" % (num) if num > 1 else "queryContent_1-"
                url = re.sub("queryContent_[0-9]*-", s, url)
                # print(cnum)
            val = driver.find_element_by_xpath('(//ul[@class="pages-list"]/li)[1]').text
            # print(url)
            driver.get(url)
            # time.sleep(1)
            # print("1111")
            locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            # print("22222")

            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            ul = soup.find("ul", class_="article-list2")
            trs = ul.find_all("li")
            data = []
            for li in trs:
                try:
                    info_number = li.find("span", class_="blue-w").text
                    info = re.findall(r"\[(.*)\]", info_number)[0]
                except:
                    info = ""
                a = li.find("a")
                title = a["title"]
                link = a["href"]
                try:
                    date = li.find("div", class_="list-times").text
                except:
                    date = li.find("p", class_="bmZhong").text

                tmp = [info.strip(), title.strip(), date.strip(), link.strip()]
                data.append(tmp)
            df = pd.DataFrame(data=data)
            return df
        else:
            driver.get("http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=265")
            url = driver.current_url
            num = num - 58
            s = "queryContent_%d-" % (num) if num > 1 else "queryContent_1-"
            url = re.sub("queryContent_[0-9]*-", s, url)
            val = driver.find_element_by_xpath('(//ul[@class="pages-list"]/li)[1]').text
            # print(url)
            driver.get(url)
            # time.sleep(1)
            # print("1111")
            try:
                locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1][string()!='%s']" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                pass
            # print("22222")

            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            ul = soup.find("ul", class_="article-list2")
            trs = ul.find_all("li")
            data = []
            for li in trs:
                try:
                    info_number = li.find("span", class_="blue-w").text
                    info = re.findall(r"\[(.*)\]", info_number)[0]
                except:
                    info = ""
                a = li.find("a")
                title = a["title"]
                link = a["href"]
                
                try:
                    date = li.find("div", class_="list-times").text
                except:
                    date = li.find("p", class_="bmZhong").text

                tmp = [info.strip(), title.strip(), date.strip(), link.strip()]
                data.append(tmp)
            df = pd.DataFrame(data=data)
            return df
    else:
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            ul = soup.find("ul", class_="article-list2")
            trs = ul.find_all("li")
            data = []
            for li in trs:
                try:
                    info_number = li.find("span", class_="blue-w").text
                    info = re.findall(r"\[(.*)\]", info_number)[0]
                except:
                    info = ""
                a = li.find("a")
                title = a["title"]
                link = a["href"]
                
                try:
                    date = li.find("div", class_="list-times").text
                except:
                    date = li.find("p", class_="bmZhong").text

                tmp = [info.strip(), title.strip(), date.strip(), link.strip()]
                data.append(tmp)
            df = pd.DataFrame(data=data)
            return df



def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    url = driver.current_url
    if ("channelId=264") in url:
        locator = (By.XPATH, '(//ul[@class="pages-list"]/li)[1]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page_1 = re.findall('/(\d+)', page_all)[0]
        # print(page)
        driver.get("http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=265")
        time.sleep(3)
        locator = (By.XPATH, '(//ul[@class="pages-list"]/li)')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, '(//ul[@class="pages-list"]/li)[1]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page_2 = re.findall('/(\d+)', page_all)[0]
        page = int(page_1) + int(page_2)
        driver.quit()
        return page
    else:
        locator = (By.XPATH, '(//ul[@class="pages-list"]/li)')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            locator = (By.XPATH, '(//ul[@class="pages-list"]/li)[1]')
            page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            # print(url)
            page = re.findall('/(\d+)', page_all)[0]
            # print(page)
        except Exception as e:
            page = "1"
        driver.quit()
        return int(page)




def f3(driver,url):
    driver.get(url)
    locator=(By.XPATH,"//div[@class='content clearfix']")

    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(locator))

 
    try:

        driver.switch_to.frame(0)
        page=driver.page_source

        before=len(driver.page_source)
        time.sleep(0.1)
        after=len(driver.page_source)
        i=0
        while before!=after:
            before=len(driver.page_source)
            time.sleep(0.3)
            after=len(driver.page_source)
            i+=1
            if i>10:break
        page=driver.page_source

        soup=BeautifulSoup(page,'lxml')
        div=soup.find('body')
        return div
    except:
        pass


    before=len(driver.page_source)
    time.sleep(0.1)
    after=len(driver.page_source)
    i=0
    while before!=after:
        before=len(driver.page_source)
        time.sleep(0.2)
        after=len(driver.page_source)
        i+=1
        if i>5:break

    page=driver.page_source

    soup=BeautifulSoup(page,'lxml')
    #
    div=soup.find('div',class_='content clearfix')
    
    
    return div

data = [
        ["gcjs_zhaobiao_gg",
        "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=264",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        # ["gcjs_yaoqingzhaobiao_gg",
        #  "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=265",
        #  ["info", "name", "ggstart_time", "href"]],
        ["gcjs_zigeyushen_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=266",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["gcjs_biangeng_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=272",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["gcjs_dayi_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=267",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["gcjs_zishenjiegou_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=270",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["gcjs_zhongbiaohx_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=269",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["gcjs_zhongbiao_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=271",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["gcjs_hetongliyue_gg",
        "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=349",
        ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],

        ["zfcg_yucai_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=344",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["zfcg_zhaobiao_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=274",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["zfcg_biangeng_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=276",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["zfcg_zhongbiao_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=275",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["zfcg_hetong_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=278",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],
        ["zfcg_yanshou_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=277",
         ["diqu", "name", "href","ggstart_time","ggend_time","info"],f1,f2],

    ]


# driver=webdriver.Chrome()
# url="http://www.ytggzyjy.gov.cn:9082/jyxxgcdy/76516.jhtml"

# driver.get(url)


def work(conp,**args):
    #est_meta(conp,data=data,diqu="山东省烟台市",num=5**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","yantai"])

#est_tbs(conp=["postgres","since2015","127.0.0.1","shandong","yantai"],data=data,total=1,num=1)
