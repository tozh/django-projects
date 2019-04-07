# from pymongo import MongoClient
# from collections import OrderedDict
#
#
# class Person():
#     def __init__(self, id, ip='127.0.0.1', port=27017):
#         self.id = id
#
#         self.person = {}
#         self.followers = []
#         self.followees = []
#
#         client = MongoClient(ip, port)
#         self.query_db(client)
#         client.close()
#
#     def query_db(self, client):
#         db = client.zhihu
#         self.person = db.users.find_one({'_id':self.id})
#         if self.person:
#             followers_query = db.followers.find_one({'_id':self.id})
#             if followers_query:
#                 self.followers = followers_query['value']['data']
#
#             followees_query = db.followees.find_one({'_id':self.id})
#             if followees_query:
#                 self.followees = followees_querzy['value']['data']
#
#     def to_dict(self):
#         result = OrderedDict()
#         result['meta'] = {'query': 'person'}
#         result['id'] = self.id
#         result['data'] = self.person
#         result['followers'] = self.followers
#         result['followees'] = self.followees
#         return result
#
# if __name__ == '__main__':
#     p = Person('luvddd', 'localhost', 27017)
