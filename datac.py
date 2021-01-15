import time
import json
import requests

url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
html = requests.get(url)
data = json.loads(html.json()['data'])
china_data = data['areaTree'][0]['children']
data_set = []
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