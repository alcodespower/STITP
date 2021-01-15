from flask import Flask
import time
import json
import requests
from flask_cors import *
from flask import Flask, render_template, redirect, request, url_for , send_file
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 激活环境

# !/usr/bin/env python3.8
# -*- coding: utf-8 -*-

app = Flask(__name__)
def getTime():
    return int(round(time.time() * 1000))

@app.route('/')
def hello_guy():
    return 'Hey,Guy!Go Away Now!'

@app.route('/data_set')
def data_set():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
    html = requests.get(url)
    data = json.loads(html.json()['data'])
    china_data = data['areaTree'][0]['children']
    data_set = []
    data_set2 = []
    for i in china_data:
        data_dict = {}
        data_dict['province'] = i['name']
        data_dict['nowConfirm'] = i['total']['nowConfirm']
        data_dict['confirm'] = i['total']['confirm']
        data_dict['dead'] = i['total']['dead']
        data_dict['heal'] = i['total']['heal']
        data_dict['deadRate'] = i['total']['deadRate']
        data_dict['healRate'] = i['total']['healRate']
        data_set.append(data_dict)
    print(data_set)
    # data_dict = data_dict.json()
    data_set =  json.dumps(data_set,ensure_ascii=False)
    print(type(data_set))
    return data_set

@app.route('/skillness')
def skillness():
    url = 'https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0O0F01&sj=2019'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }  # 浏览器代理
    r = requests.get(url, headers=headers, verify=False)

    Cookie = r.headers['Set-Cookie']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Cookie': Cookie
    }  # 浏览器代理
    key = {}  # 参数键值对
    key['m'] = 'QueryData'
    key['dbcode'] = 'hgnd'
    key['rowcode'] = 'zb'
    key['colcode'] = 'sj'
    key['wds'] = '[]'
    key['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST13"}]'
    key['k1'] = str(getTime())
    r = requests.get(url, headers=headers, params=key, verify=False)
    js = json.loads(r.text)
    return js


@app.route('/skillname')
def skillname():
    url = 'https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0O0F01&sj=2019'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }  # 浏览器代理
    r = requests.get(url, headers=headers, verify=False)
    Cookie = r.headers['Set-Cookie']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Cookie': Cookie
    }  # 浏览器代理
    key = {}  # 参数键值对
    key['m'] = 'QueryData'
    key['dbcode'] = 'hgnd'
    key['rowcode'] = 'zb'
    key['colcode'] = 'sj'
    key['wds'] = '[]'
    key['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST13"}]'
    key['k1'] = int(round(time.time() * 1000))
    r = requests.get(url, headers=headers, params=key, verify=False)
    js = json.loads(r.text)
    length = len(js["returndata"]["datanodes"])
    list_2 = js['returndata']['wdnodes'][0]['nodes']
    index_list = []
    for i_2 in range(len(list_2)):
        index = list_2[i_2]['cname']
        index_list.append(index)
        # print(index)

    # 获取列名称
    list_3 = js['returndata']['wdnodes'][1]['nodes']
    columns_list = []
    for i_2 in range(len(list_2)):
        columns = list_2[i_2]['cname']
        columns_list.append(columns[:-3]) #去掉"发病率"三个字符
        print(columns)
    str_json = json.dumps(columns_list, indent=2, ensure_ascii=False)  # json转为string
    return str_json

@app.route('/nowConfirm')
def nowConfirm():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
    html = requests.get(url)
    data = json.loads(html.json()['data'])
    china_data = data['areaTree'][0]['children']
    data_nowConfirm = []
    for i in china_data:
        data_dict = {}
        data_dict['name'] = i['name']
        data_dict['value'] = i['total']['nowConfirm']
        data_nowConfirm.append(data_dict)
    print(data_nowConfirm)
    # data_dict = data_dict.json()
    data_nowConfirm =  json.dumps(data_nowConfirm,ensure_ascii=False)
    print(type(data_nowConfirm))
    return data_nowConfirm



if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    CORS(app, supports_credentials = True)
    app.run(debug=True)
