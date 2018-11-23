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

from lmfscrap import web


# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]





def f1(driver, num):
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
    print(url)
    page_1 = 58
    if "channelId=264" in url:
        locator = (By.XPATH, '(//ul[@class="pages-list"]/li)[1]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page_1 = re.findall('/(\d+)', page_all)[0]
    page_2 = int(page_1)
    if ("channelId=264"in url) or ("channelId=265" in url):
        print('1111')
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
                print("1111")
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
        return int(page)


def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,  # 表名
        "col": col,  # 字段名
        "conp": conp,  # 数据库连接
        "num": 20,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg",
        "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=264",
         ["info", "name", "ggstart_time", "href"]],
        # ["gcjs_yaoqingzhaobiao_gg",
        #  "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=265",
        #  ["info", "name", "ggstart_time", "href"]],
        ["gcjs_zigeyushen_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=266",
         ["info", "name", "ggstart_time", "href"]],
        ["gcjs_biangeng_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=272",
         ["info", "name", "ggstart_time", "href"]],
        ["gcjs_dayi_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=267",
         ["info", "name", "ggstart_time", "href"]],
        ["gcjs_zishenjiegou_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=270",
         ["info", "name", "ggstart_time", "href"]],
        ["gcjs_zhongbiaohx_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=269",
         ["info", "name", "ggstart_time", "href"]],
        ["gcjs_zhongbiao_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=271",
         ["info", "name", "ggstart_time", "href"]],
        ["gcjs_hetongliyue_gg",
        "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=349",
        ["info", "name", "ggstart_time", "href"]],

        ["zfcg_yucai_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=344",
         ["info", "name", "ggstart_time", "href"]],
        ["zfcg_zhaobiao_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=274",
         ["info", "name", "ggstart_time", "href"]],
        ["zfcg_biangeng_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=276",
         ["info", "name", "ggstart_time", "href"]],
        ["zfcg_zhongbiao_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=275",
         ["info", "name", "ggstart_time", "href"]],
        ["zfcg_hetong_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=278",
         ["info", "name", "ggstart_time", "href"]],
        ["zfcg_yanshou_gg",
         "http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=277",
         ["info", "name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
        print(data)
    for w in data:
        general_template(w[0], w[1], w[2], conp)


# conp = []

if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","yantai"]

    work(conp=conp, i=1)

    # driver=webdriver.Chrome()
    # url="http://www.ytggzyjy.gov.cn:9082/queryContent_1-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=264"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # for i in range(1, 10):
    #     df=f1(driver, i)
    #     print(df)
