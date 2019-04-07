# from pymongo import MongoClient
# from collections import OrderedDict
# import re
# from bson.son import SON
#
# class TopPerson():
#     def __init__(self, sort, limit=20, ip='127.0.0.1', port=27017, **kwargs):
#         self.sort = sort
#         self.limit = limit
#         self.kwargs = kwargs
#
#         client = MongoClient(ip, port)
#         self.query_db(client)
#         client.close()
#
#     def query_db(self, client):
#         db = client.zhihu
#         match = {}
#         for k, v in self.kwargs.items():
#             match[k] = v
#
#         pipeline = [
#             {'$sort': SON([(self.sort, -1)])},
#             {'$match': match},
#             {'$limit': int(self.limit)},
#         ]
#
#         self.top_person = list(db.users.aggregate(pipeline))
#
#     def to_dict(self):
#         result = OrderedDict()
#         result['meta'] = {'query': 'top-person'}
#         result['sort'] = self.sort
#         result['limit'] = self.limit
#         result['kwargs'] = self.kwargs
#         result['data'] = self.top_person
#         return result
