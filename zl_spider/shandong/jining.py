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

from shandong_v1.fake_useragent import agents


def f1(driver, num):
    print(num)
    url = driver.current_url
    id = re.findall(r'CategoryCode=(\d+)', url)[0]
    # print(id)
    if id == "503000":
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
    elif id == "553001":
        # print("111")
        id_1 = "002002"
        page_num1 = get_pageall(id)
        page_num2 = get_pageall(id_1)
        if num <= page_num1:
            # print("222")
            data_1 = get_data(id, num)
            # print(data_1)
            df = pd.DataFrame(data=data_1)
            return df
        elif page_num1 < num <= (page_num1+page_num2):
            data_2 = get_data(id_1, (num - page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df
        else:
            # print("3333")
            id_3 = "002902"
            data_3 = get_data(id_3, (num-(page_num1+page_num2)))
            # print(data_2)
            df = pd.DataFrame(data=data_3)
            return df

    elif id == "552001":
        # print("111")
        id_1 = "002004"
        page_num1 = get_pageall(id)
        page_num2 = get_pageall(id_1)
        if num <= page_num1:
            # print("222")
            data_1 = get_data(id, num)
            # print(data_1)
            df = pd.DataFrame(data=data_1)
            return df
        elif page_num1 < num <= (page_num1+page_num2):
            data_2 = get_data(id_1, (num - page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df
        else:
            # print("3333")
            id_3 = "002904"
            data_3 = get_data(id_3, (num-(page_num1+page_num2)))
            # print(data_2)
            df = pd.DataFrame(data=data_3)
            return df
    elif id == "551001":
        # print("111")
        id_1 = "002901"
        page_num1 = get_pageall(id)
        page_num2 = get_pageall(id_1)
        if num <= page_num1:
            # print("222")
            data_1 = get_data(id, num)
            # print(data_1)
            df = pd.DataFrame(data=data_1)
            return df
        elif page_num1 < num <= (page_num1+page_num2):
            data_2 = get_data(id_1, (num - page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df
        else:
            # print("3333")
            id_3 = "00200101"
            data_3 = get_data(id_3, (num-(page_num1+page_num2)))
            # print(data_2)
            df = pd.DataFrame(data=data_3)
            return df
    elif id == "551002":
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
            id_1 = "007001"
            data_2 = get_data(id_1, (num-page_num1))
            # print(data_2)
            df = pd.DataFrame(data=data_2)
            return df
    elif id == "553002":
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
            id_1 = "007002"
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
        'Cookie': 'Abp.Localization.CultureName=zh-CN; UM_distinctid=166bd5a0a591df-06018582a40a3b-68101b7d-1fa400-166bd5a0a5ac63; ASP.NET_SessionId=rnp3pfk0em1sm3pq5mbzmfxo; __RequestVerificationToken=ScDJhFUQHal-xpcDsZZauTKRLdbSRuTF42lP5MQyzAzFfjahmqwGSQW310biEwNoF8sS82aB8tXASg_feKHK0hWo21CkiZrW4JufL88WVCY1; CNZZDATA1273473557=292458821-1540772995-%7C1540806026; Public-XSRF-TOKEN=pXeTT4CHYm4zShxYJjvYzVyUalwAgwUQRS7rxjKackrhszOSUaKgpKS4ZsGxkiAjDjCOTdoyNcOIy93ju8Zq5z0DQUEGCXmQtMM5Z_sSKFQ1',
        # 'Host':'www.jnggzyjy.gov.cn',
        # 'Origin':'http://www.jnggzyjy.gov.cn',
        'Public-X-XSRF-TOKEN': 'pXeTT4CHYm4zShxYJjvYzVyUalwAgwUQRS7rxjKackrhszOSUaKgpKS4ZsGxkiAjDjCOTdoyNcOIy93ju8Zq5z0DQUEGCXmQtMM5Z_sSKFQ1',
        # 'Referer':'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=511001',
        # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        # 'X-Requested-With':'XMLHttpRequest',
    }
    data = {
        "FilterText": "",
        "categoryCode": "{}".format(id),
        "maxResultCount": 20,
        "skipCount": (num - 1) * 20,
        "tenantId": "3",
    }
    sesion = requests.session()
    res = sesion.post(url=start_url, headers=headers, data=data)
    # 需要判断是否为登录后的页面

    if res.status_code == 200:
        html = res.text
        # print(html)
        datas = []
        if html:
            # print(type(html))
            html = json.loads(html)
            data = html["result"]
            # print(type(data))
            table = data["items"]
            # print(table)
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
    if id == "503000":
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
    elif id == "553001":
        page_num1 = get_pageall(id)
        id_1 = "002002"
        page_num2 = get_pageall(id_1)
        id_2 = "002902"
        page_num3 = get_pageall(id_2)
        page_num = page_num1 + page_num2 + page_num3
        return page_num
    elif id == "552001":
        page_num1 = get_pageall(id)
        id_1 = "002004"
        page_num2 = get_pageall(id_1)
        id_2 = "002904"
        page_num3 = get_pageall(id_2)
        page_num = page_num1 + page_num2 + page_num3
        return page_num
    elif id == "551001":
        page_num1 = get_pageall(id)
        id_1 = "00200101"
        page_num2 = get_pageall(id_1)
        id_2 = "002901"
        page_num3 = get_pageall(id_2)
        page_num = page_num1 + page_num2 + page_num3
        return page_num
    elif id == "551002":
        page_num1 = get_pageall(id)
        id_1 = "007001"
        page_num2 = get_pageall(id_1)
        page_num = page_num1 + page_num2
        return page_num
    elif id == "553002":
        page_num1 = get_pageall(id)
        id_1 = "007002"
        page_num2 = get_pageall(id_1)
        page_num = page_num1 + page_num2
        return page_num
    elif id == "553003":
        page_num1 = get_pageall(id)
        id_1 = "005002"
        page_num2 = get_pageall(id_1)
        page_num = page_num1 + page_num2
        return page_num
    elif id == "551003":
        page_num1 = get_pageall(id)
        id_1 = "005001"
        page_num2 = get_pageall(id_1)
        page_num = page_num1 + page_num2
        return page_num

    else:
        page_num = get_pageall(id)
        return page_num



def get_pageall(id):
    # id = re.findall(r'CategoryCode=(\d+)', start_url)[0]
    cookie_list = driver.get_cookies()
    print(cookie_list)
    # cookie_dict = {cookie["name"]:cookie["value"] for cookie in cookie_list}
    cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
    print(cookie)
    cookiestr = '; '.join(item for item in cookie)
    print(cookiestr)

    user_agent = random.choice(agents)
    start_url = "http://www.jnggzyjy.gov.cn/api/services/app/stPrtBulletin/GetBulletinList"

    headers = {
        'Cookie':"Abp.Localization.CultureName=zh-CN; ASP.NET_SessionId=rvcuq4b2wjac3xbmeqghrtom; __RequestVerificationToken=QIeDvfhDb3y4TxR0GQf7tOivbSMBnmE93Hlk_UHQdSmopDWlRv60XbYqKRlPMUKHdilLIpw4AR1ENoytQVTesy2_yRcEiXLdXVi4tt8pCKI1; UM_distinctid=1670fcebff1371-0e3b0dfe360d03-68101b7d-1fa400-1670fcebff290; CNZZDATA1273473557=1150960343-1542154004-%7C1542154004; Public-XSRF-TOKEN=IT1lj9BCcMcbFnN-0G8ehXLNfKvu3-a0sQWMi1mGi0QRnyexut8pfSXvxOAA-yzbNlapXFQgmXp9SAEiWLhpNycq4QH_fKCpl8kcoIqohKI1",
        'User-Agent': user_agent,
        # 'Cookie': 'Abp.Localization.CultureName=zh-CN; UM_distinctid=166bd5a0a591df-06018582a40a3b-68101b7d-1fa400-166bd5a0a5ac63; ASP.NET_SessionId=rnp3pfk0em1sm3pq5mbzmfxo; __RequestVerificationToken=ScDJhFUQHal-xpcDsZZauTKRLdbSRuTF42lP5MQyzAzFfjahmqwGSQW310biEwNoF8sS82aB8tXASg_feKHK0hWo21CkiZrW4JufL88WVCY1; CNZZDATA1273473557=292458821-1540772995-%7C1540806026; Public-XSRF-TOKEN=pXeTT4CHYm4zShxYJjvYzVyUalwAgwUQRS7rxjKackrhszOSUaKgpKS4ZsGxkiAjDjCOTdoyNcOIy93ju8Zq5z0DQUEGCXmQtMM5Z_sSKFQ1',
        # 'Host':'www.jnggzyjy.gov.cn',
        # 'Origin':'http://www.jnggzyjy.gov.cn',
        'Public-X-XSRF-TOKEN': 'pXeTT4CHYm4zShxYJjvYzVyUalwAgwUQRS7rxjKackrhszOSUaKgpKS4ZsGxkiAjDjCOTdoyNcOIy93ju8Zq5z0DQUEGCXmQtMM5Z_sSKFQ1',
        # 'Referer':'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=511001',
        # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        # 'X-Requested-With':'XMLHttpRequest',
    }
    data = {
        "FilterText": "",
        "categoryCode": "{}".format(id),
        "maxResultCount": 20,
        "skipCount": 0,
        "tenantId": "3",
    }
    sesion = requests.session()
    res = sesion.post(url=start_url, headers=headers, data=data)
    # 需要判断是否为登录后的页面
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
        ["gcjs_zhaobiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=503000",
         ["name", "code", "ggstart_time", "href"]],

        ["gcjs_biangeng_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=503002",
         ["name", "code", "ggstart_time", "href"]],

        ["gcjs_dayi_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=504002",
         ["name", "code", "ggstart_time", "href"]],

        ["gcjs_zhongbiaohuoxuanren_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=511001",
         ["name", "code", "ggstart_time", "href"]],

        ["gcjs_zhongbiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=513001",
         ["name", "code", "ggstart_time", "href"]],

        ["zfcg_zhaobiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=551001",
         ["name", "code", "ggstart_time", "href"]],

        ["zfcg_biangeng_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=552001",
         ["name", "code", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=553001",
         ["name", "code", "ggstart_time", "href"]],

        ["ylcg_zhaobiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=551002",
         ["name", "code", "ggstart_time", "href"]],

        ["ylcg_biangeng_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=552002",
         ["name", "code", "ggstart_time", "href"]],

        ["ylcg_zhongbiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=553002",
         ["name", "code", "ggstart_time", "href"]],

        ["qsydw_zhaobiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=551003",
         ["name", "code", "ggstart_time", "href"]],

        ["qsydw_biangeng_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=552003",
         ["name", "code", "ggstart_time", "href"]],

        ["qsydw_zhongbiao_gg", "http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=553003",
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
    # conp=["postgres","since2015","192.168.3.171","shandong","jining"]
    #
    # work(conp=conp)

    driver=webdriver.Chrome()
    url="http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=553002"
    driver.get(url)
    df = f2(driver)
    print(df)
    # for i in range(17, 20):
    #     df=f1(driver, i)
    #     print(df)
