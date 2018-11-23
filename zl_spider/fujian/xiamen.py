import random

import pandas as pd
import re

import requests
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
from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="xiamen"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
from fake_useragent import agents




def f1(driver, num):
    url = driver.current_url
    if "getMongoGovPurchaseNoticePage.do/" in url:
        payloadData = payload_Data(url, num)
        url = url.rsplit('/', maxsplit=1)[0]
    else:
        payloadData = payload_Data(url, num)
    user_agent = random.choice(agents)
    headers = {
        # 'Cookie': cookiestr,
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
        'Host': 'zyjy.xmas.gov.cn',
    }

    sesion = requests.session()
    res = sesion.post(url=url, headers=headers, data=json.dumps(payloadData))
    # 需要判断是否为登录后的页面
    data_list = []
    if res.status_code == 200:
        html = res.text
        if html:
            if "getMongoGovPurchaseNoticePage.do" in url:
                html = json.loads(html)
                data = html["data"]
                datalist = data["datalist"]
                # print(noticeType)
                for data in datalist:
                    purchaserName = data['projCode']
                    projName = data['projName']
                    publishTime = data['publishTime']
                    link = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/governBid.do?noticeId=" + data['noticeId'] + "&noticeType=" +\
                           "{}".format(noticeType) + "&projCode=" + data['projCode'] + "&projId=" + data['projId']

                    tmp = [purchaserName, projName, publishTime, link]
                    data_list.append(tmp)
            else:
                html = json.loads(html)
                data = html["data"]
                datalist = data["dataList"]
                for data in datalist:
                    if "getConstructInfoPage.do" in url:
                        tenderProjCode = data['projCode']
                        projName = data['projName']
                        pubDate = data['recordDate']
                        link = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/registerInfo.do?" + "projId=" + data['projId'] + "&dataFrom=" + str(data['dataFrom'])
                    elif "/getNoticePage.do" in url:
                        tenderProjCode = data['tenderProjCode']
                        projName = data['projName']
                        pubDate = data['SEND_TIM']
                        link = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/agentBid.do?leftIndex=F006" + "&uniqueId=" + data['uniqueId']

                    else:
                        leftIndex = ""
                        if "getBltPage.do" in url:
                            leftIndex = "leftIndex=F001"
                        elif "getAnQuestionPage_project.do" in url:
                            leftIndex = "leftIndex=F002"
                        elif "getEvaBulletinPage.do" in url:
                            leftIndex = "leftIndex=F004"
                        elif "getwinBulletinPage_project.do" in url:
                            leftIndex = "leftIndex=F005"
                        tenderProjCode = data['tenderProjCode']
                        projName = data['projName']
                        try:
                            pubDate = data['pubDate']
                        except:
                            pubDate = data['sendTime']
                        link = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/agentBid.do?" + leftIndex + "&uniqueId=" + data['uniqueId'] + "&objId=" + data['bid']

                    tmp = [tenderProjCode, projName, pubDate, link]
                    data_list.append(tmp)
                    # print(tmp)

    df = pd.DataFrame(data_list)
    df['info'] = None
    return df


def payload_Data(url, num):
    if "getMongoGovPurchaseNoticePage.do/" in url:
        global noticeType
        noticeType = re.findall(r'/(\d+)', url)[0]
        payloadData = {'pageIndex': "{}".format(num), 'pageSize': "10", 'noticeTitle': "", 'regionCode': "", 'tenderType': "D", 'transType': "", 'pubTime': "",
                       'state': "", 'noticeType': "{}".format(noticeType), 'purchaseType': "", 'searchBeginTime': "", 'searchEndTime': ""}
        return payloadData
    elif "getConstructInfoPage.do" in url:
        payloadData = {'pageIndex':"{}".format(num),'pageSize':"10",'classId':0,'centerId':0,'projNo':"",'projName':"",'ownerDeptName':"",'showRange':"",'searchBeginTime':"",'searchEndTime':""}
    elif "getNoticePage.do" in url:
        payloadData = {'pageIndex':"{}".format(num),'pageSize':"10",'centerId':0,'projName':"",'title':"",'showRange':""}
    else:
        payloadData = {'pageIndex': "{}".format(num), 'pageSize': "10", 'projName': "", 'centerId': 0, 'showRange': "",'tenderProjType': "", 'searchBeginTime': "", 'searchEndTime': ""}

    return payloadData


def f2(driver):
    url = driver.current_url
    payloadData = payload_Data(url, 1)
    if "getMongoGovPurchaseNoticePage.do/" in url:
        url = url.rsplit('/', maxsplit=1)[0]
    num = get_pageall(url, payloadData)

    driver.quit()
    return num


def get_pageall(url, payloadData):
    user_agent = random.choice(agents)
    headers = {
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
        'Host': 'zyjy.xmas.gov.cn',
        }

    sesion = requests.session()
    res = sesion.post(url=url, headers=headers, data=json.dumps(payloadData))
    # 需要判断是否为登录后的页面
    # datas = []
    # print(res)
    if res.status_code == 200:
        html = res.text
        # print(html)
        if html:
            if "getMongoGovPurchaseNoticePage.do" in url:
                html = json.loads(html)
                data = html["data"]
                total = int(data["pagecount"])
                if total / 10 == int(total / 10):
                    page_all = int(total / 10)
                else:
                    page_all = int(total / 10) + 1
                return page_all
            else:
                html = json.loads(html)
                data = html["data"]
                total = int(data["totalPage"])

                return total


def f3(driver, url):
    driver.get(url)
    if "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/governBid.do?" in url:

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

        div = soup.find('div', class_="info")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    elif "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/agentBid.do?" in url:

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

        div = soup.find('div', id="contentStr")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    elif "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/registerInfo.do?" in url:

        locator = (By.CLASS_NAME, "buildTitle")
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

        div = soup.find('div', style="margin: 30px 30px 5px 30px;")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    else:

        locator = (By.ID, "iframepage")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

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

        div = soup.find('iframe', id="iframepage")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div


data = [
    ["gcjs_yuzhaobiao_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/construct/getConstructInfoPage.do",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/project/getBltPage.do",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_biangen_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/project/getAnQuestionPage_project.do",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/project/getEvaBulletinPage.do",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/project/getwinBulletinPage_project.do",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/project/getNoticePage.do",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_zhaobiao_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/govermentPurchase/getMongoGovPurchaseNoticePage.do/1",
    ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zhongbiao_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/govermentPurchase/getMongoGovPurchaseNoticePage.do/2",
    ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/govermentPurchase/getMongoGovPurchaseNoticePage.do/4",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省厦门市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","xiamen"])

    # driver=webdriver.Chrome()
    # # url = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/govermentPurchase/getMongoGovPurchaseNoticePage.do/2"
    # url = "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/project/getNoticePage.do"
    # driver.get(url)
    # # df = f3(driver, "http://zyjy.xmas.gov.cn/XmUiForWeb2.0/xmebid/registerInfo.do?projId=40288a16670adc050167106045c30003&dataFrom=1")
    # # df = f2(driver)
    # # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
