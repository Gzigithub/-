import random

import pandas as pd
import re

import requests
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

import json
from zhulong.util.etl import add_info, est_meta, est_html, est_tbs, gg_existed

_name_="nanan"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
from fake_useragent import agents



def f1(driver, num):
    url = driver.current_url
    payloadData,noticeType = payload_Data(url, num)
    start_url = url.rsplit('/', maxsplit=1)[0]
    user_agent = random.choice(agents)
    # start_url = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/construct/getConstructInfoPage.do"
    headers = {
        # 'Cookie': cookiestr,
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
        'Host': 'www.nazbcg.gov.cn',
    }

    sesion = requests.session()
    res = sesion.post(url=start_url, headers=headers, data=json.dumps(payloadData))
    # 需要判断是否为登录后的页面
    data_list = []
    if res.status_code == 200:
        html = res.text
        if html:
            if "getTenderInfoPage.do" in url:
                html = json.loads(html)
                data = html["data"]
                datalist = data["datalist"]
                # print(noticeType)
                for data in datalist:
                    projName = data['noticeTitle']
                    publishTime = data['sendTime']
                    try:
                        proj_id = data['proj_id']
                    except:
                        proj_id = ""
                    try:
                        pre_evaId = data['pre_evaId']
                    except:
                        pre_evaId = ""
                    try:
                        evaId = data['evaId']
                    except:
                        evaId = ""
                    try:
                        signUpType = data['signUpType']
                    except:
                        signUpType = ""
                    link = "http://www.nazbcg.gov.cn/hyweb/naebid/bidDetails.do?flag=1&tenderProjCode=" + data['tenderProjCode'] + "&tenderProjId=" +\
                        data['tenderProjId'] + "&proj_id=" + proj_id +"&pre_evaId=" + pre_evaId+ "&evaId=" + evaId + "&signUpType=" + signUpType

                    tmp = [projName, publishTime, link]
                    data_list.append(tmp)

            elif "getMongoGovPurchaseNoticePage.do/z" in url:
                html = json.loads(html)
                data = html["data"]
                datalist = data["datalist"]
                # print(noticeType)
                for data in datalist:
                    projName = data['noticeTitle']
                    publishTime = data['publishTime']
                    link = "http://www.nazbcg.gov.cn/hyweb/commons/simpleBidDetails.do?handle=1&projId=" + data['projId'] + "&noticeType=" + "{}".format(noticeType)
                    tmp = [projName, publishTime, link]
                    data_list.append(tmp)
                    # print(tmp)

            elif "getMongoGovPurchaseNoticePage.do/g" in url:
                if int(noticeType) != 6:
                    html = json.loads(html)
                    data = html["data"]
                    datalist = data["datalist"]
                    # print(noticeType)
                    for data in datalist:
                        projName = data['noticeTitle']
                        publishTime = data['publishTime']

                        try:
                            isCatch = data['isCatch']
                            link ="http://www.nazbcg.gov.cn/hyweb/commons/simpleBidDetails.do?handle="+data['isCatch']+"&projId=" + data['projId'] + "&noticeType=" + "{}".format(noticeType)
                        except:
                            link = "http://www.nazbcg.gov.cn/hyweb/commons/mongoGovBid.do?projId=" + data['projId'] + "&flag=2"
                        tmp = [projName, publishTime, link]
                        data_list.append(tmp)
                    # print(tmp)
                else:
                    html = json.loads(html)
                    data = html["data"]
                    datalist = data["datalist"]
                    # print(noticeType)
                    for data in datalist:
                        projName = data['noticeTitle']
                        publishTime = data['publishTime']
                        link = "http://www.nazbcg.gov.cn/hyweb/commons/simpleBidDetails.do?handle=4&projId=" + data['projId'] + "&noticeType=6"
                        tmp = [projName, publishTime, link]
                        data_list.append(tmp)

            else:
                html = json.loads(html)
                data = html["data"]
                datalist = data["datalist"]
                # print(noticeType)
                for data in datalist:
                    projName = data['title']
                    publishTime = data['publishTime']
                    link = "http://www.nazbcg.gov.cn/hyweb/naebid/otherBid.do?srcNoticeId=" + data['noticeId'] + "&noticeType=" + "{}".format(noticeType)
                    tmp = [projName, publishTime, link]
                    data_list.append(tmp)


    df = pd.DataFrame(data_list)
    df['info'] = None
    return df


def payload_Data(url, num):

    if "/getTenderInfoPage.do/j=" in url:

        noticeType = re.findall(r'/j=(\d+)', url)[0]

        payloadData = {'pageIndex':"{}".format(num),'pageSize':"10",'noticeTitle':"",'regionCode':"350500",'tenderType':"G",'transType' :"",'pubTime' :"",'state' :"",'noticeType' :"{}".format(noticeType),'tradeCode':"1"}
        return payloadData,noticeType

    elif "/getTenderInfoPage.do/x=" in url:

        noticeType = re.findall(r'/x=(\d+)', url)[0]

        payloadData = {'pageIndex':"{}".format(num),'pageSize':"10",'noticeTitle':"",'regionCode':"350500",'tenderType':"G",'transType' :"",'pubTime' :"",'state' :"",'noticeType' :"{}".format(noticeType),'tradeCode':"2"}
        return payloadData,noticeType

    elif "/getMongoGovPurchaseNoticePage.do/z=" in url:

        noticeType = re.findall(r'/z=(\d+)', url)[0]

        payloadData = {'pageIndex':"{}".format(num),'pageSize':"10",'noticeTitle':"",'regionCode':"350500",'tenderType':"D",'transType' :"",'pubTime' :"",'state' :"",'noticeType' :"{}".format(noticeType)}
        return payloadData,noticeType

    elif "/getMongoGovPurchaseNoticePage.do/g=" in url:

        noticeType = re.findall(r'/g=(\d+)', url)[0]

        payloadData = {'pageIndex':"{}".format(num),'pageSize':"10",'noticeTitle':"",'regionCode':"350500",'tenderType':"DD",'transType' :"",'pubTime' :"",'state' :"",'noticeType' :"{}".format(noticeType)}
        return payloadData,noticeType

    elif "/getOtherTradeNoticePage.do/q=" in url:

        noticeType = re.findall(r'/q=(\d+)', url)[0]

        payloadData = {'pageIndex':"{}".format(num),'pageSize':"10",'noticeTitle':"",'regionCode':"350500",'tenderType':"Z",'transType' :"",'pubTime' :"",'state' :"",'noticeType' :"{}".format(noticeType)}
        return payloadData,noticeType



def f2(driver):
    url = driver.current_url
    payloadData,noticeType = payload_Data(url, 1)
    # print(url)

    url = url.rsplit('/', maxsplit=1)[0]
    num = get_pageall(url, payloadData)

    driver.quit()
    return num


def get_pageall(url, payloadData):

    user_agent = random.choice(agents)
    headers = {
        # 'Cookie': cookiestr,
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
        'Host': 'www.nazbcg.gov.cn',
        }
    sesion = requests.session()
    res = sesion.post(url=url, headers=headers, data=json.dumps(payloadData))
    # 需要判断是否为登录后的页面
    if res.status_code == 200:
        html = res.text
        # print(html)
        if html:
            html = json.loads(html)
            data = html["data"]
            total = int(data["pagecount"])
            # print(total / 20)
            if total / 10 == int(total / 10):
                page_all = int(total / 10)
            else:
                page_all = int(total / 10) + 1
                # print(page_all)
            return page_all


def f3(driver, url):
    driver.get(url)
    if "http://www.nazbcg.gov.cn/hyweb/naebid/otherBid.do?srcNoticeId=" in url:

        locator = (By.CLASS_NAME, "info")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i = 0
        while before != after:
            before = len(driver.page_source)
            time.sleep(0.1)
            after = len(driver.page_source)
            i += 1
            if i > 5: break

        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find('div', id="main")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    elif "http://www.nazbcg.gov.cn/hyweb/commons/simpleBidDetails.do" in url:

        locator = (By.CLASS_NAME, "info")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))


        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i = 0
        while before != after:
            before = len(driver.page_source)
            time.sleep(0.1)
            after = len(driver.page_source)
            i += 1
            if i > 5: break

        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find('div', id="main")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    else:
        locator = (By.CLASS_NAME, "info")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

        html = driver.page_source
        html_data = etree.HTML(html)
        data = html_data.xpath("//ul[@id='LoutiNav']/li/a/text()")

        div_list = []
        for ti in data:
            if '1' in ti:
                title = re.findall(r'(.*)\(1\)', ti)[0]
                driver.find_element_by_link_text('{}'.format(ti)).click()
                locator = (By.CLASS_NAME, "info")
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

                before = len(driver.page_source)
                time.sleep(0.1)
                after = len(driver.page_source)
                i = 0
                while before != after:
                    before = len(driver.page_source)
                    time.sleep(0.1)
                    after = len(driver.page_source)
                    i += 1
                    if i > 5: break

                page = driver.page_source
                soup = BeautifulSoup(page, 'lxml')
                div = soup.find('div', class_="details_content")

                a = {"{}".format(title): str(div)}
                div_list.append(a)
        div_list = json.dumps(div_list, ensure_ascii=False)

        return div_list


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.nazbcg.gov.cn/hyweb/transInfo/getTenderInfoPage.do/j=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "http://www.nazbcg.gov.cn/hyweb/transInfo/getTenderInfoPage.do/j=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.nazbcg.gov.cn/hyweb/transInfo/getTenderInfoPage.do/j=3",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://www.nazbcg.gov.cn/hyweb/transInfo/getTenderInfoPage.do/j=4",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_xiaoer_gg",
     "http://www.nazbcg.gov.cn/hyweb/transInfo/getTenderInfoPage.do/x=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_gg",
     "http://www.nazbcg.gov.cn/hyweb/transInfo/getTenderInfoPage.do/x=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_xiaoer_gg",
     "http://www.nazbcg.gov.cn/hyweb/transInfo/getTenderInfoPage.do/x=3",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg",
     "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/z=1",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/z=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangen_gg",
     "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/z=4",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_gg",
     "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/g=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_yucai_gg",
     "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/g=6",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_jieguo_gg",
     "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/g=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhaobiao_gg",
     "http://www.nazbcg.gov.cn/hyweb/otherTrade/getOtherTradeNoticePage.do/q=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_jieguo_gg",
     "http://www.nazbcg.gov.cn/hyweb/otherTrade/getOtherTradeNoticePage.do/q=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省南安市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","nanan"])

    #
    # driver=webdriver.Chrome()
    # # url = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/govermentPurchase/getMongoGovPurchaseNoticePage.do/2"
    # url = "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/g=1"
    # driver.get(url)
    # df = f3(driver, "http://www.nazbcg.gov.cn/hyweb/naebid/bidDetails.do?flager=1&tenderProjCode=G350583893622001&tenderProjId=44166B1A-94D9-3A7B-0429-4DC4CC82A91F&proj_id=-6123&pre_evaId=&evaId=-1958&signUpType=0")
    # print(df)
    # df = f2(driver)
    # print(df)
    # driver=webdriver.Chrome()
    # # url = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/govermentPurchase/getMongoGovPurchaseNoticePage.do/2"
    # url = "http://www.nazbcg.gov.cn/hyweb/govPurchase/getMongoGovPurchaseNoticePage.do/g=1"
    # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
