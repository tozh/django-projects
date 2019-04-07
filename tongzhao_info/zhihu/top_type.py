# from pymongo import MongoClient
# from collections import OrderedDict
# import re
# from bson.son import SON
#
#
# class TopType():
#     def __init__(self, type, limit=20, ip='127.0.0.1', port=27017):
#         self.type = type
#         self.limit = limit
#         self.top_type = []
#
#         client = MongoClient(ip, port)
#         self.query_db(client)
#         client.close()
#
#     def query_db(self, client):
#         db = client.zhihu
#         pipeline = [
#             {'$sort': SON([('num', -1)])},
#             {'$limit': self.limit}
#         ]
#         self.top_type = list(db[self.type].aggregate(pipeline))
#
#     def to_dict(self):
#         result = OrderedDict()
#         result['meta'] = {'query': 'top-' + self.type}
#         result['type'] = self.type
#         result['limit'] = self.limit
#         result['data'] = self.top_type
#         return result
