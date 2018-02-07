# coding=utf-8
import redis
import hashlib

class Item_dump():

    def __init__(self, item):
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=4) # 连接数据库
        self.item_key = "item_dumpkey"
        self.item = item

    def item_dump(self):
        f = hashlib.sha1()
        f.update(str(self.item).encode())
        fingerprint = f.hexdigest()
        added = self.r.sadd(self.item_key, fingerprint)
        # 保存成功返回false， 保存失败返回True
        return added == 0


if __name__ == '__main__':
    item = {"_id":2}
    i = Item_dump(item)
    ret = i.item_dump()
    print(ret)




