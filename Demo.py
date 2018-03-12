import requests

url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&cardNum=&iname=%E6%9D%AD%E5%B7%9E%E5%A4%AA%E8%A1%8C%E5%BB%BA%E7%AD%91%E5%B7%A5%E7%A8%8B%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&areaName=&ie=utf-8&oe=utf-8&format=json&t=1520386794507&cb=jQuery110205081241129331773_1520386766284&_=1520386766286'

json = requests.get(url)

print(json.content.decode())

