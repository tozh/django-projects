# from pymongo import MongoClient
# from collections import OrderedDict
# import re
#
#
# class Type():
#     def __init__(self, type, id='', name='', ip='127.0.0.1', port=27017):
#         self.type = type
#         self.id = id
#         self.name = name
#
#         self.entity = {}
#
#         client = MongoClient(ip, port)
#         self.query_db(client)
#         client.close()
#
#     def query_db(self, client):
#         db = client.zhihu
#
#         if self.id:
#             self.entity = db[self.type].find_one({'_id': self.id})
#         elif self.name:
#             pattern = r'.*' + self.name + r'.*'
#             value = re.compile(pattern)
#             self.entity = db[self.type].find_one({'name': value})
#
#     def to_dict(self):
#         result = OrderedDict()
#         result['meta'] = {'query': self.type}
#         result['type'] = self.type
#         result['id'] = self.id
#         result['name'] = self.name
#         result['data'] = self.entity
#         return result