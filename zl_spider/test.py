# coding=gbk
#

# num_list = [245, 301, 332, 366, 415, 465, 474, 483]
# num = 481
# list_num = int(len(num_list))
# for i in range(1, list_num+1):
#     print(i)
#     if i == 1:
#         if num <= num_list[i - 1]:
#             print('1111')
#             num = num
#             print(num)
#             # f1_data(driver, i)
#             # return num
#
#     else:
#         if num_list[i-2] < num <= num_list[i-1]:
#             print('333')
#             num = num - num_list[i - 2]
#             print(num)
            # f1_data(driver, i)
            # return num

# a = [1, 2, 3, 4, 5]
# c= []
# for i in range(1, len(a)+1):
#     b = sum(a[:i])
#     c.append(b)
#
# print(c)
import copy
import re
# #
num = 14

url = "�������http://www.bidding.gov.cn/qtjygg/132201.htm"
url = re.findall(r'(http.*)', url)[0].strip()
print(url)
# #
# str = "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004002/004002010/004002010002/info=10"
# num = int(re.findall(r'info=(\d+)', str)[0])
# print(num)
# from functools import wraps
# def zhongbiao_gg(f):
#     def wrap(*krg):
#
#         driver = krg[0]
#         print(driver)
#         return f(*krg)
#
#     return wrap
#
# @zhongbiao_gg
# def f1(driver,num):
#     pass
#
# f1(1,3)
#
# str = '...46'
# num = re.findall(r'(\d+)', str)[0]
# print(num)

#
# list_1 = [[1,2,4], [4,5,7], [4,5,6]]
# list_2 = [[7,5,8], [7,8,9], [7,5,1]]
#
# list_3 = list_1 + list_2
# print(list_3)

# str = "��ǰҳ��?22/226??��?435?��??��һҳ?ת����ҳ"
#
# p = re.findall(r'(\d+)/', str)[0]
# print(p)
#
# total = 4001
# print(total/20)
# if total/20 == int(total/20):
#     print("www")
#     print(int(total/20))
# else:
#     page_all = int(total/20) + 1
#     print(page_all)

# str_1 = "http://www.ytggzyjy.gov.cn:9082/queryContent_3-jyxxZc.jspx?title=&inDates=&ext=&origin=&channelId=344"
# str = "http://www.ytggzyjy.gov.cn:9082/queryContent_84-jyxx.jspx?title=&inDates=&ext=&origin=&channelId=269"
# page = re.findall("queryContent_(.*)-", str)[0]
# print(page)


# str = "http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/004002001001/MoreInfo.aspx?CategoryNum=004002001001"
#
# d = str.rsplit('/', maxsplit=1)[0]
# print(d)
# page_all = "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-0?pageIndex=683"
# url = "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-0?pageIndex=6"
# # print(type(int(page_all)))
# page = re.findall('pageIndex=(.*)', page_all)[0]
# # print(page)
# num = 341
# s = "pageIndex=%d" % (num) if num > 1 else "pageIndex=1"
# url = re.sub("pageIndex=[0-9]*", s, url)
# print(int(page))
# print(url)
# import pandas as pd
#
# """http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002001/079002001007/?Paging=1
# http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002001/079002001007"""
#
# url = "http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002001/079002001007/?Paging=1"
# # if "Paging" in url:
# print("111")
# url_2 = re.sub(r"(\?Paging=.)", "?Paging=", url)
# # url_3 = url.rsplit('/', maxsplit=1)[0]
# # print(url_2)
# print(url_2)

# url = "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002002/about.html"
# # cnum = int(re.findall("/([0-9]{1,}).html", url)[0])
# num = 1
# s = "%d.html"%(num) if num>1 else "index.html"
# url = re.sub("about[0-9]*.html", s, url)
# print(url)
#
# a = [[['�ĳǾ��ü�������������ˮ�������ﻧ�����쿱����Ŀ��ζ�������5��15��סլ��2����ҵ2��', '2018-08-16', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=f09d1487-0e37-411e-9c2f-41831e9021ba&categoryNum=079001001001003'], ['�ĳǾ��ü�������������ˮ�������ﻧ�����쿱����Ŀ��ζ�������5��15��סլ��2����ҵ2��', '2018-07-20', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=2eb9e9ac-520d-4301-a181-67d162f39ffd&categoryNum=079001001001003'], ['�ĳǾ��ü�������������ˮ�������ﻧ�����쿱����Ŀ', '2018-06-28', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=79e9fe89-eef2-486b-9083-b0144a745d85&categoryNum=079001001001003'], ['�ĳǾ��ü�������������ˮ�������ﻧ������滮ʩ��ͼ�����Ŀ', '2018-06-15', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=28e8f89e-308c-44a0-a845-ea67847c210f&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ˮ�������ۼ�ʩ��ͼ��ơ�������Ŀ�����Σ�', '2018-05-08', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=fd5e050c-6986-4951-abfc-517f6aa01710&categoryNum=079001001001003'], ['�ĳǾ��ü����������̾���Ƭ���滮�����ۼ�ʩ��ͼ��ơ�������Ŀ', '2018-04-09', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=69920c96-cc50-4b02-86b4-7b14a5516d3a&categoryNum=079001001001003'], ['�ĳǾ��ü����������¶��ܲ�ҵ԰һ�ڿ�����Ŀ', '2018-04-04', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=b09dda7b-7255-4a8c-b74f-5309f0f8b2a5&categoryNum=079001001001003'], ['�ĳǾ��ü����������¶��ܲ�ҵ԰һ�ڿ�����Ŀ', '2018-03-09', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=e90c5807-a37b-45ad-815e-f0b170dd055a&categoryNum=079001001001003'], ['�ĳǾ��ü����������¶��ܲ�ҵ԰һ��ʩ��ͼ�����Ŀ�ĳǾ��ü����������¶��ܲ�ҵ԰һ��ʩ��ͼ���', '2018-03-09', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=4e7f1c2d-b2f4-4a75-a3c5-457f70474143&categoryNum=079001001001003'], ['�ĳǾ��ü����������¶��ܲ�ҵ԰�滮���������������������Ŀ', '2018-02-28', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=21582367-3c03-4c70-b196-af82ad77cb66&categoryNum=079001001001003'], ['�ĳǾ��ü�������������·�����ﻧ��������Ŀ����ʩ��ͼ�����Ŀ', '2018-02-05', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=c6d0d8ad-465a-491e-a326-640f2351f3e1&categoryNum=079001001001003'], ['�ĳǾ��ü�������������·�����ﻧ��������Ŀ����ʩ��ͼ�����Ŀ', '2018-01-02', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=c951da5d-68cd-4789-9f1b-f5b0b5390059&categoryNum=079001001001003'], ['�ܹ���ũó��ˮ��ˡ������г����ۺ�����Ŀ���', '2017-12-29', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=38349e8e-3ffa-4057-b15a-b96ab9384904&categoryNum=079001001001003'], ['�ܹ���ũó�Ƕ�Ʒ�г�����������������Ŀ���', '2017-12-29', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=bfcd6f77-ed7e-4553-b585-6a288369c1c9&categoryNum=079001001001003'], ['�ĳǹ��ʽ�������D�ؿ鿱����Ŀ', '2017-12-13', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=f17b11b9-46aa-47a8-b962-2c4f05a26b12&categoryNum=079001001001003'], ['¡��̩��԰סլ������Ŀ', '2017-12-06', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=34070ed9-0990-4c27-bf8b-44ad327cb3ed&categoryNum=079001001001003'], ['�ĳǾ��ü��������������ͽֵ����´�����СѧУ���½��滮������������б깫��', '2017-09-12', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=42202c30-ecb1-4cd2-aadb-c3ffaa7dc5a8&categoryNum=079001001001003'], ['�ĳǾ��ü��������������ͽֵ����´���ѧУ���½��滮������������б�����', '2017-09-12', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=c947632d-47bb-462c-b14f-bb4d86a35fe6&categoryNum=079001001001003'], ['�ĳǹ��ʽ������Ĺ滮����������ʩ��ͼ�����Ŀ', '2017-09-11', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=9dc8ceec-a2dc-4369-a367-d9017ae670ef&categoryNum=079001001001003'], ['�ĳǾ��ü�������������ˮ����ڿ�����Ŀ', '2017-08-17', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=82b01d96-b97d-4098-b2bf-6223aeabc21c&categoryNum=079001001001003']], [['�ĳǾ��ü�����������Է�³Ƕ���16#-17#��ס¥����ҵ����������Ŀ', '2017-08-10', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=307f9afb-bf67-48e2-b00c-3bf0dd3640ee&categoryNum=079001001001003'], ['�ĳǾ��ü�����������Է�³Ƕ���16#-17#��ס¥����ҵ����ʩ��ͼ�����Ŀ', '2017-07-14', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=5c4916d9-78e8-42f1-95c5-eb41313aba3b&categoryNum=079001001001003'], ['�ĳǾ��ü�������������ˮ����ڿ�����Ŀ', '2017-07-14', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=10c90773-f5b6-4eec-82e2-17c5b0aad1a6&categoryNum=079001001001003'], ['�ĳǾ��ü�������������ˮ�����ʩ��ͼ�����Ŀ', '2017-07-14', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=37f3e4df-f298-405e-ba9d-794a35e3d94f&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ˮ�����޽�����ϸ�滮���������Ŀ', '2017-06-28', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=5e4c7658-e2ee-4a1c-871e-0e401edd7953&categoryNum=079001001001003'], ['¡��̩��԰סլ�����Ŀ', '2017-05-18', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=1f3a9229-d66a-4ba8-9206-369858da3fc2&categoryNum=079001001001003'], ['�ĳǾ��ü����������������¹�Ԣ��Ƭ������ʩ������������������������', '2017-03-10', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=2f86d0ae-2712-4681-91c4-a111f96ea0b9&categoryNum=079001001001003'], ['�ĳǾ��ü����������������¹�Ԣ��Ƭ������ʩ�������������', '2017-01-25', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=7f443804-004b-4da2-b6c5-0014d53c2847&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ������ʩ��ͼ�����Ŀ�б깫��', '2017-01-22', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=443c26ad-5b09-433e-9c45-806b9b00a70d&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ�����쿱����Ŀ�б깫��', '2017-01-22', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=d835eec9-c6a7-4399-a049-a45487976e90&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ������ʩ��ͼ�����Ŀ', '2016-10-31', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=d4696f52-cc25-4013-87ee-250e0fa5324b&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ������ʩ��ͼ�����Ŀ', '2016-10-31', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=81af2ae5-d181-4ba8-b4de-a3f5161db6f8&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ�����쿱����Ŀ', '2016-10-28', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=0a003131-fbfa-4d46-8229-a55900babd64&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ�����쿱����Ŀ', '2016-10-28', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=7aa2504b-7603-4497-93c7-3d1d05224aff&categoryNum=079001001001003'], ['���������ﻧ��������Ŀ�����ڣ�ʩ��ͼ�����Ŀ�б깫��', '2016-05-04', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=f050461e-4f7c-4c75-b638-2bacb4484537&categoryNum=079001001001003'], ['�����������ﻧ�����죨һ�����ڣ����⾰�������Ŀ�б깫��', '2016-05-04', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=eb3873ae-03ae-4c39-8981-fa8e75b47448&categoryNum=079001001001003'], ['���������ﻧ��������Ŀ�����ڣ�������Ŀ �б깫��', '2016-05-04', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=7b3cdd3f-5853-45b4-88fe-3d06e8defa3e&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ�������޽�����ϸ�滮���������Ŀ(����)�б깫��', '2016-04-26', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=ec06a44f-6d99-41b7-a754-c3598e96cdd3&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ�������޽�����ϸ�滮���������Ŀ(����)�б깫��', '2016-04-26', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=226b5606-b8be-4d68-a8d0-499344902f9a&categoryNum=079001001001003'], ['�ĳǾ��ü�����������ׯ�������ﻧ�������޽�����ϸ�滮���������Ŀ�б깫��', '2016-04-15', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=acc3b95c-425b-4600-84cf-5045890897ff&categoryNum=079001001001003']], [['�ĳǾ��ü�����������ׯ�������ﻧ�������޽�����ϸ�滮���������Ŀ�б깫��', '2016-04-15', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=aea0ef14-bc47-4dac-b91c-ac8e7d195b2a&categoryNum=079001001001003'], ['�ĳǾ��ü�����������̫������ʩ��ͼ�����Ŀ�б깫��', '2016-03-21', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=8f5d2dcf-7819-4e12-b881-aa58ef0b6f40&categoryNum=079001001001003'], ['�ĳǾ��ü�����������̫�����ڿ�����Ŀ', '2016-03-21', 'http://www.lcsggzyjy.cn/lcweb//ztbinfo/ZtbDyDetail_jsgc.aspx?type=1&infoid=ee4af398-7c32-44ce-a049-4f9e63ec1edf&categoryNum=079001001001003']]]
#
# # print(len(a))
# # print(a[0])
# list_1 = []
# for i in a:
#     for j in i:
#         list_1.append(j)
#
# print(list_1)
# df = pd.DataFrame(data=list_1)
#
# print(df)

# a = [1, 2, 3, ['a', 'b', ['A', 'B']]]
a = (1, 2, 3)

b = a
c = copy.copy(a)
d = copy.deepcopy(a)


# a[3][2].append('C')

print(a)
print(b)
print(c)
print(d)



