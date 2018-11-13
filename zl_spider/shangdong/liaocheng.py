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
    # 获取当前页的url
    url = driver.current_url
    if "Paging" in url:
        # print(url)
        url_3 = url.rsplit('/', maxsplit=2)[0]
        # print(url_3)
        driver.get(url_3)
    try:
        locator = (By.XPATH, '(//a[@class="span6-item-link l"])[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        pass
    # 获取当前页的url
    print(url)
    locator = (By.XPATH, '(//td[@class="MoreinfoColor"]/a)[{}]'.format(num))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
    # url_link = driver.find_element_by_xpath('(//td[@class="MoreinfoColor"]/a)[{}]'.format(num)).click()
    # print(url)
    locator = (By.XPATH, '//a[@class="bread-link"][5]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    if "本栏目暂时没有内容！" in html:
        url_s = driver.current_url
        url_3 = url_s.rsplit('/', maxsplit=2)[0]
        print(url_3)
        driver.get(url_3)
        time.sleep(1)
        return
    else:
        page_num = driver.find_element_by_xpath('//td[@class="huifont"]').text
        # 获取总页数
        page = re.findall('/(.*)', page_num)[0]
        # print(page)
        data_list = []
        for i in range(int(page) + 1):
            if i == 0:
                continue
            else:
                # print(i)
                df = f1_data(driver, i)
                # print(df)
                data_list.append(df)
        # print(data_list)

        data = []
        for i in data_list:
            for j in i:
                data.append(j)

        df = pd.DataFrame(data=data)
        # print(df)
        return df


def f1_data(driver, i):
    url_i = driver.current_url
    # print(url_i)
    if "Paging" not in url_i:
        # print(url)
        url_2 = url_i.rsplit('/', maxsplit=1)[0]
        # print(url_3)
        url_1 = url_2 + "/?Paging={}".format(i)
        # print(url_1)
        driver.get(url_1)
    else:
        url_1 = re.sub(r"(\?Paging=[0-9]*)", "?Paging={}".format(i), url_i)
        val = driver.find_element_by_xpath('(//a[@class="span6-item-link l"])[1]').text
        # print(url)
        driver.get(url_1)
        locator = (By.XPATH, "(//a[@class='span6-item-link l'])[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # print(url_1)
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, 'lxml')
    ul = soup.find("div", class_="content")
    tb = ul.find_all("div",recursive=False)[0]
    lis = tb.find_all("tr")
    data = []
    for li in lis:
        # print(li)
        a = li.find("a")

        title = a["title"]
        # print(a["title"])
        link = "http://www.lcsggzyjy.cn" + a["href"]
        span = li.find("font")
        tmp = [title, span.text.strip(), link]
        data.append(tmp)


    return data

    #     cnum=1
    # else:
    #     cnum=int(re.findall("/([0-9]{1,}).html", url)[0])
    # if num!=cnum:
    #     if num==1:
    #         url=re.sub("[0-9]*.html","about.html",url)
    #     else:
    #         s = "%d.html" % (num) if num > 1 else "index.html"
    #         url = re.sub("about[0-9]*.html", s, url)
    #         # print(cnum)
    #     val = driver.find_element_by_xpath("(//div[@class='ewb-info-a']/a)[1]").text
    #     # print(url)
    #     driver.get(url)
    #     time.sleep(2)
    #
    #     locator = (By.XPATH, "(//div[@class='ewb-info-a']/a)[1][string()!='%s']" % val)
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))





def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """

    locator = (By.XPATH, '//td[@class="MoreinfoColor"]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    html_data = etree.HTML(html)
    page = html_data.xpath('//td[@class="MoreinfoColor"]/a/text()')
    num = len(page)

    return int(num)


def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,  # 表名
        "col": col,  # 字段名
        "conp": conp,  # 数据库连接
        "num": 15,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        # ["gcjs_zhaobiao_kanchasheji_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001001/079001001001/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhaobiao_shigong_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001001/079001001002/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhaobiao_jianli_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001001/079001001003/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhaobiao_huowu_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001001/079001001004/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhaobiao_qita_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001001/079001001005/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_biangeng_kanchasheji_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001002/079001002001/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_biangeng_shigong_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001002/079001002002/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_biangeng_jianli_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001002/079001002003/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_biangeng_huowu_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001002/079001002004/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_biangeng_qita_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001002/079001002005/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhongbiao_kanchasheji_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001003/079001003001/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhongbiao_shigong_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001003/079001003002/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhongbiao_jianli_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001003/079001003003/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhongbiao_huowu_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001003/079001003004/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhongbiao_qita_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001003/079001003005/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_biaoqian_kanchasheji_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001004/079001004001/",
        #  ["name", "ggstart_time", "href"]],
        ["gcjs_biaoqian_shigong_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001004/079001004002/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_biaoqian_jianli_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001004/079001004003/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_biaoqian_huowu_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001004/079001004004/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_biaoqian_qita_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001004/079001004005/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_liubiao_kanchasheji_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001005/079001005001/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_liubiao_shigong_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001005/079001005002/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_liubiao_jianli_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001005/079001005003/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_liubiao_huowu_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001005/079001005004/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_liubiao_qita_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001005/079001005005/",
         ["name", "ggstart_time", "href"]],
        ["zfcg_zhaobiao_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002001/",
         ["name", "ggstart_time", "href"]],
        ["zfcg_biangeng_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002002/",
         ["name", "ggstart_time", "href"]],
        ["zfcg_zhongbiao_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002003/",
         ["name", "ggstart_time", "href"]],
        ["zfcg_feibiao_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002004/",
         ["name", "ggstart_time", "href"]],
        ["zfcg_xinxigongkai_gg", "http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002006/",
         ["name", "ggstart_time", "href"]],


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
    conp=["postgres","since2015","192.168.3.171","shandong","liaocheng"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002001/"
    # driver.get(url)
    # for i in range(1,4):
    #     df=f1(driver, i)
    #     print(df)
