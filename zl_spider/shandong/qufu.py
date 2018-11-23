import json
import random
import time

import pandas as pd
import re

import requests
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
from zl_spider.shangdong.fake_useragent import agents


def f1(driver, num):
    print(num)
    url = driver.current_url
    id = re.findall(r'CategoryCode=(\d+)', url)[0]
    # print(id)
    if id == "552001":
        # print("111")
        id_1 = "002004"
        page_num1 = get_pageall(id_1)
        if num <= page_num1:
            # print("222")
            data_1 = get_data(id_1, num)
            # print(data_1)
            df = pd.DataFrame(data=data_1)
            return df
        else:
            # print("3333")
            id_2 = "002904"
            data_2 = get_data(id_2, (num-page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df

    elif id == "551001":
        # print("111")
        id_1 = "002901"
        datas = get_data(id_1, num)
        df = pd.DataFrame(data=datas)
        return df

    elif id == "553001":
        print("111")
        id_1 = "002902"
        page_num1 = get_pageall(id_1)
        if num <= page_num1:
            print("222")
            data_1 = get_data(id_1, num)
            # print(data_1)
            df = pd.DataFrame(data=data_1)
            return df
        else:
            print("3333")
            id_2 = "002002"
            data_2 = get_data(id_2, (num-page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df

    elif id == "503000":
        # print("111")
        page_num1 = get_pageall(id)
        if num <= page_num1:
            # print("222")
            data_1 = get_data(id, num)
            # print(data_1)
            df = pd.DataFrame(data=data_1)
            return df
        else:
            # print("3333")
            id_1 = "001001"
            data_2 = get_data(id_1, (num-page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df

    elif id == "511001":
        # print("111")
        page_num1 = get_pageall(id)
        if num <= page_num1:
            # print("222")
            data_1 = get_data(id, num)
            # print(data_1)
            df = pd.DataFrame(data=data_1)
            return df
        else:
            # print("3333")
            id_1 = "001002"
            data_2 = get_data(id_1, (num-page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df

    else:
        datas = get_data(id, num)
        df = pd.DataFrame(data=datas)
        return df




def get_data(id, num):
    user_agent = random.choice(agents)
    start_url = "http://www.jnggzyjy.gov.cn/api/services/app/stPrtBulletin/GetBulletinList"

    headers = {
        # 'Cookie': cookiestr,
        'User-Agent': user_agent,
        'Cookie':'Abp.Localization.CultureName=zh-CN; ASP.NET_SessionId=m1131mz3oijy0szk04qoe5j2; __RequestVerificationToken=M3w3qWf_PisGP3Oria-7xQ3pf6Ip3u0w08xBjbZPXTYX5VUgZE7Ty0zBMO_1zXciYHfFsHVbY-oir7etbDRXXlTMaqNLM1UzIwEAoEbC9Kw1; Public-XSRF-TOKEN=-RSVwuDUYfSxBv8HxRN5yAaA4VM3PAto-H-1Hc1kDxQFVTMyvzfDS1zc2a_1OcB8Jmne3HMDkwPalWXI6l0xOOiMX2ni8vCB1-tfyDJf0YQ1; UM_distinctid=166c4886295f5-0a362c74ecbee4-68101b7d-1fa400-166c4886296273; CNZZDATA1273473557=160814158-1540890505-%7C1540890505',
        'Host':'www.jnggzyjy.gov.cn',
        # 'Origin':'http://www.jnggzyjy.gov.cn',
        'Public-X-XSRF-TOKEN':'-RSVwuDUYfSxBv8HxRN5yAaA4VM3PAto-H-1Hc1kDxQFVTMyvzfDS1zc2a_1OcB8Jmne3HMDkwPalWXI6l0xOOiMX2ni8vCB1-tfyDJf0YQ1',
        # 'Referer':'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=511001',
        # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        # 'X-Requested-With':'XMLHttpRequest',
    }
    data = {
        "FilterText": "",
        "categoryCode": "{}".format(id),
        "maxResultCount": 20,
        "skipCount": (num - 1) * 20,
        "tenantId": "11",
    }
    sesion = requests.session()
    res = sesion.post(url=start_url, headers=headers, data=data)
    # 需要判断是否为登录后的页面
    if res.status_code == 200:
        html = res.text
        datas = []
        if html:
            # print(type(html))
            html = json.loads(html)
            data = html["result"]
            table = data["items"]
            for data_dict in table:

                td_1 = data_dict["code"]
                td_2 = data_dict["id"]
                td_3 = data_dict["releaseDate"]
                try:
                    date_l = re.findall(r'(\d+.*)T', td_3)[0]
                except:
                    date_l = td_3
                td_4 = data_dict["title"]
                td_5 = data_dict["categoryCode"]
                "http://www.jnggzyjy.gov.cn/JiNing/Bulletins/Detail/566846de-c45d-b4e9-2aef-39e8497e4baa/?CategoryCode=511001"
                prjName_link = "http://www.jnggzyjy.gov.cn/JiNing/Bulletins/Detail/" + td_2 + "/?CategoryCode=" + td_5

                data = [td_4, td_1, date_l, prjName_link]

                datas.append(data)
        return datas
    # print(datas)
    # df = pd.DataFrame(data=datas)
    # return df


def f2(driver):
    start_url = driver.current_url
    id = re.findall(r'CategoryCode=(\d+)', start_url)[0]
    if id == "552001":
        # page_num1 = get_pageall(id)
        id_1 = "002004"
        page_num2 = get_pageall(id_1)
        id_2 = "002904"
        page_num3 = get_pageall(id_2)
        page_num = page_num2 + page_num3
        return page_num
    elif id == "551001":
        # page_num1 = get_pageall(id)
        id_1 = "002901"
        page_num2 = get_pageall(id_1)
        page_num = page_num2
        return page_num
    elif id == "553001":
        # page_num1 = get_pageall(id)
        id_1 = "002002"
        page_num2 = get_pageall(id_1)
        id_2 = "002902"
        page_num3 = get_pageall(id_2)
        page_num = page_num2 + page_num3
        return page_num
    elif id == "503000":
        page_num1 = get_pageall(id)
        id_1 = "001001"
        page_num2 = get_pageall(id_1)
        page_num = page_num1 + page_num2
        return page_num
    elif id == "511001":
        page_num1 = get_pageall(id)
        id_1 = "001002"
        page_num2 = get_pageall(id_1)
        page_num = page_num1 + page_num2
        return page_num

    else:
        page_num = get_pageall(id)
        return page_num



def get_pageall(id):
    # id = re.findall(r'CategoryCode=(\d+)', start_url)[0]
    # cookie_list = driver.get_cookies()
    # print(cookie_list)
    # cookie_dict = {cookie["name"]:cookie["value"] for cookie in cookie_list}
    # cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
    # print(cookie)
    # cookiestr = '; '.join(item for item in cookie)
    # print(cookiestr)

    user_agent = random.choice(agents)
    start_url = "http://www.jnggzyjy.gov.cn/api/services/app/stPrtBulletin/GetBulletinList"

    headers = {
        # 'Cookie': cookiestr,
        'User-Agent': user_agent,
        # 'Accept':'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate',
        # 'Accept-Language':'zh-CN,zh;q=0.9',
        # 'Connection':'keep-alive',
        # 'Content-Length':'91',
        # 'Content-Type':'application/json',
        'Cookie':'Abp.Localization.CultureName=zh-CN; ASP.NET_SessionId=m1131mz3oijy0szk04qoe5j2; __RequestVerificationToken=M3w3qWf_PisGP3Oria-7xQ3pf6Ip3u0w08xBjbZPXTYX5VUgZE7Ty0zBMO_1zXciYHfFsHVbY-oir7etbDRXXlTMaqNLM1UzIwEAoEbC9Kw1; Public-XSRF-TOKEN=-RSVwuDUYfSxBv8HxRN5yAaA4VM3PAto-H-1Hc1kDxQFVTMyvzfDS1zc2a_1OcB8Jmne3HMDkwPalWXI6l0xOOiMX2ni8vCB1-tfyDJf0YQ1; UM_distinctid=166c4886295f5-0a362c74ecbee4-68101b7d-1fa400-166c4886296273; CNZZDATA1273473557=160814158-1540890505-%7C1540890505',
        'Host':'www.jnggzyjy.gov.cn',
        # 'Origin':'http://www.jnggzyjy.gov.cn',
        'Public-X-XSRF-TOKEN':'-RSVwuDUYfSxBv8HxRN5yAaA4VM3PAto-H-1Hc1kDxQFVTMyvzfDS1zc2a_1OcB8Jmne3HMDkwPalWXI6l0xOOiMX2ni8vCB1-tfyDJf0YQ1',
        # 'Referer':'http://www.jnggzyjy.gov.cn/QuFu/Bulletins?CategoryCode=553001',
        # 'X-Requested-With':'XMLHttpRequest',
    }
    data = {
        "FilterText": "",
        "categoryCode": "{}".format(id),
        "maxResultCount": 20,
        "skipCount": 0,
        "tenantId": "11",
    }
    sesion = requests.session()
    res = sesion.post(url=start_url, headers=headers, data=data)
    # 需要判断是否为登录后的页面
    # print(res)
    # datas = []
    if res.status_code == 200:
        html = res.text
        if html:
            # print(type(html))
            html = json.loads(html)
            data = html["result"]
            # print(type(data))
            total = int(data["totalCount"])
            # print(total / 20)
            if total / 20 == int(total / 20):
                page_all = int(total / 20)
            else:
                page_all = int(total / 20) + 1
                # print(page_all)
            return page_all


def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,  # 表名
        "col": col,  # 字段名
        "conp": conp,  # 数据库连接
        "num": 5,  # 线程数量
        # "total": 100,  # 测试用，只测试100页

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg", "http://www.jnggzyjy.gov.cn/QuFu/Bulletins?CategoryCode=503000",
         ["name", "code", "ggstart_time", "href"]],

        ["gcjs_zhongbiao_gg", "http://www.jnggzyjy.gov.cn/QuFu/Bulletins?CategoryCode=511001",
         ["name", "code", "ggstart_time", "href"]],

        ["zfcg_zhaobiao_gg", "http://www.jnggzyjy.gov.cn/QuFu/Bulletins?CategoryCode=551001",
         ["name", "code", "ggstart_time", "href"]],

        ["zfcg_biangeng_gg", "http://www.jnggzyjy.gov.cn/QuFu/Bulletins?CategoryCode=552001",
         ["name", "code", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg", "http://www.jnggzyjy.gov.cn/QuFu/Bulletins?CategoryCode=553001",
         ["name", "code", "ggstart_time", "href"]],


    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
        print(data)
    for w in data:
        general_template(w[0], w[1], w[2], conp)



if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","qufu"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.jnggzyjy.gov.cn/QuFu/Bulletins?CategoryCode=553001"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
