# coding=utf-8

import requests
from rand_ua import Rand_ua
import time
from handel_json import Handel_json
import pymongo
from item_dump import Item_dump
import datetime
from read_company import read_company2
import sys


proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H65403216IJKN42D"
proxyPass = "55697F9CCB86225E"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
  "host" : proxyHost,
  "port" : proxyPort,
  "user" : proxyUser,
  "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}

'''
https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&
query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&
cardNum=&
iname=%E5%B9%BF%E8%A5%BF%E5%9B%BD%E6%B4%B2%E6%8A%95%E8%B5%84%E7%AE%A1%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&areaName=&
ie=utf-8&
oe=utf-8&
format=json&
t=1517968939734&
cb=jQuery1102025075011778413225_1517966791832&
_=1517966791839
2147895

resource_id:6899
query:失信被执行人名单
cardNum:
iname:广西国洲投资管理有限公司
areaName:
ie:utf-8
oe:utf-8
format:json
t:1517968939734
cb:jQuery1102025075011778413225_1517966791832
_:1517966791839
2147895
706967
resource_id:6899
query:失信被执行人名单
cardNum:
iname:广西国洲投资管理有限公司
areaName:
ie:utf-8
oe:utf-8
format:json
t:1517969646702
cb:jQuery1102025075011778413225_1517966791832
_:1517966791840
2854862
429919
resource_id:6899
query:失信被执行人名单
cardNum:
iname:江苏梵克雅宝纺织科技发展有限公司
areaName:
ie:utf-8
oe:utf-8
format:json
t:1517970076623
cb:jQuery1102025075011778413225_1517966791832
_:1517966791842
3284781
'''

class Sx_baidu_spider():

    def __init__(self, path=None, type=None, text_list=None, code=1517966791832):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.conn = self.client["qg_ss"]['company']
        self.type = type # 公司类型
        self.text_list = text_list # 测试列表
        self.path = path # 公司名单路径
        self.code = code # url参数（每天都会变）不变也不影响

    def get_json(self):
        company_list = read_company2(self.path)
        for c in company_list:
            company = c.strip()
            if company:
                i = Item_dump(company)
                ret = i.item_dump()
                if not ret:
                    item = {}
                    item["company"] = company
                    item["type"] = self.type
                    nd = int(time.time()) * 1000
                    nd1 = nd + 2500000
                    url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&cardNum=&iname={}&areaName=&ie=utf-8&oe=utf-8&format=json&t={}&cb=jQuery1102025075011778413225_{}&_={}".format(company, nd1,self.code, nd)
                    u = Rand_ua()
                    ua = u.rand_chose()
                    headers = {
                        "User-Agent": ua,
                    }
                    try:
                        ret = requests.get(url, headers=headers, timeout=60)
                    except Exception as e:
                        with open('log/ss_log.log','a') as f:
                            now = str(datetime.datetime.now())
                            f.write(now + ',' + str(e) + ',' + company + ',' + '失信信息' + '\n')
                        continue
                    json = ret.content.decode()
                    h = Handel_json(json, company)
                    ss_list = h.handel_json()
                    item["失信信息"] = ss_list
                    print(item)
                    self.save_mongodb(item)
                    time.sleep(3)

    # 测试模式,不保存数据库，不去重
    def get_text(self):
        if self.text_list:
            for c in self.text_list:
                company = c.strip()
                if company:
                    print(company)
                    item = {}
                    item["company"] = company
                    item["type"] = self.type
                    nd = int(time.time()) * 1000
                    nd1 = nd + 2500000

                    url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&cardNum=&iname={}&areaName=&ie=utf-8&oe=utf-8&format=json&t={}&cb=jQuery1102025075011778413225_1517966791832&_={}".format(company, nd1, nd)
                    u = Rand_ua()
                    ua = u.rand_chose()
                    headers = {
                        "User-Agent": ua,
                    }
                    try:
                        ret = requests.get(url, headers=headers)
                    except Exception as e:
                        print(e)
                        with open('log/ss_log.log','a') as f:
                            now = str(datetime.datetime.now())
                            f.write(now + ',' + str(e) + ',' + company + ',' + '失信信息' + '\n')
                        continue
                    json = ret.content.decode()
                    h = Handel_json(json, company)
                    ss_list = h.handel_json()
                    item["失信信息"] = ss_list
                    print(item)
                    time.sleep(3)

    def save_mongodb(self, item):
        self.conn.insert_one(dict(item))
        print("保存成功！")


if __name__ == '__main__':

    path = sys.argv[1]

    company_list = ["广西五鸿建设集团有限公司","昆明翔威泵业制造有限责任公司","无锡市江南容器成套有限公司","黑龙江宇林建筑工程有限责任公司","苏州尔宝电子有限公司"]
    s = Sx_baidu_spider(path=path)
    # s = Sx_baidu_spider(text_list=company_list)
    s.get_json()
    # s.get_text()




