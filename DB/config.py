from pymongo import MongoClient

NAME = 'BTM'  # 数据库名称BTM

client = MongoClient('localhost', 27017)  # 链接数据库

db = client[NAME]  # 链接BTM数据库

config = db.config  # 记录数据已同步的信息
