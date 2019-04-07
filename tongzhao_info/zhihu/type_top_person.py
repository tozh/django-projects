#
#
# from pymongo import MongoClient
# from collections import OrderedDict
# import re
# from bson.son import SON
#
# import logging
# mylog = logging.getLogger(__name__)
#
#
# # classifications are education/ business/ location
# # id/Entity: the entity of that classification
# # value : what value to be sort for top
# # list top person
#
# class TypeTopPerson():
#     def __init__(self, type, sort, id='', name='', limit=20, ip='127.0.0.1', port=27017, **kwargs):
#         self.type = type
#
#         self.sort = sort
#         self.id = id
#         self.name = name
#         self.limit = limit
#         self.kwargs = kwargs
#
#         self.entity = {}
#         self.type_top = []
#
#         client = MongoClient(ip, port)
#         self.query_db(client)
#         client.close()
#
#     def query_db(self, client):
#         db = client.zhihu
#         if self.id:
#             self.entity = db[self.type].find_one({'_id': self.id})
#         elif self.name:
#
#             pattern = r'.*' + self.name + r'.*'
#             value = re.compile(pattern)
#
#             self.entity = db[self.type].find_one({'name': value})
#
#         if self.entity:
#             if not self.id:
#                 self.id = self.entity['_id']
#
#             match = {self.type: {'id': self.id}} if self.type == 'business' else {self.type: {'$elemMatch': {'id': self.id}}}
#
#             for k, v in self.kwargs.items():
#                 match[k] = v
#
#             pipeline = [
#                 {'$sort': SON([(self.sort, -1)])},
#                 {'$match': match},
#                 {'$limit': int(self.limit)}
#             ]
#             logging.warning(pipeline)
#
#             self.type_top = list(db.users.aggregate(pipeline))
#
#
#     def to_dict(self):
#         result = OrderedDict()
#         result['meta'] = {'query': self.type + '-top_person'}
#         result['type'] = self.type
#         result['id'] = self.id
#         result['name'] = self.name
#         result['sort'] = self.sort
#         result['limit'] = self.limit
#         result['kwargs'] = self.kwargs
#         result['entity'] = self.entity
#         result['data'] = self.type_top
#         return result