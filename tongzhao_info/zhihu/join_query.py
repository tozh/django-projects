from pymongo import MongoClient
from collections import OrderedDict
import re
from bson.son import SON
import copy

import logging

mylog = logging.getLogger(__name__)


# classifications are education/ business/ location
# entity: the entity of that classification
# value : what value to be sort for top
# list top person
# -- type_top_person
class TopPersonOfEntity:
    def __init__(self, classification, value, _id='', name='', limit=20, ip='127.0.0.1', port=27017, **kwargs):
        assert classification in ['business', 'employments', 'locations', 'educations'], \
            ('API_ERROR' + '@' + 'TopPersonOfEntity: ' +
             'The <classification> parameter has error in the query.')

        assert _id or name, ('TopPersonOfEntity: ' + 'The <id> or <name> parameter has error in the query.')

        value_list = ["answer_count", "articles_count", "columns_count",
                      "question_count", "following_count", "follower_count",
                      "logs_count", "favorite_count", "participated_live_count",
                      "hosted_live_count", "following_question_count", "following_topic_count",
                      "voteup_count", "favorited_count", "thanked_count", "following_favlists_count"]
        assert value in value_list, \
            ('API_ERROR' + '@' + 'TopPersonOfEntity: ' +
             'The <value> parameter has error in the query.')

        self.classification = classification
        self.id = _id

        self.value = value
        self.name = name
        self.limit = limit
        self.kwargs = kwargs

        self.entity = {}
        self.top = []

        self.client = MongoClient(ip, port)
        self.query()
        self.client.close()

    def query(self):
        db = self.client.zhihu
        if self.id:
            self.entity = db[self.classification].find_one({'_id': self.id})
        elif self.name:
            pattern = r'.*' + self.name + r'.*'
            value = re.compile(pattern)
            self.entity = db[self.classification].find_one({'name': value})

        if self.entity:
            if not self.id:
                self.id = self.entity['_id']
            if not self.name:
                self.name = self.entity['name']

            if self.classification == 'business':
                match = {self.classification: {'id': self.id, 'name': self.name}}
            elif self.classification == 'employments':
                match = {self.classification: {'$elemMatch': {'company': {'id': self.id, 'name': self.name}}}}
            else:
                match = {self.classification: {'$elemMatch': {'id': self.id}}}

            for k, v in self.kwargs.items():
                match[k] = int(v)
            pipeline = [
                {'$sort': SON([(self.value, -1)])},
                {'$match': match},
                {'$limit': int(self.limit)}
            ]

            self.top = list(db.users.aggregate(pipeline))
        meta = {
            'query_type': 'TopPersonOfEntity',
            'database': 'zhihu',
            'classification': self.classification,
            'value': self.value,
            'limit': self.limit,
            'kwargs': self.kwargs,
            'id': self.id,
            'name': self.name
        }
        entity = self.entity

        data = self.top
        result = OrderedDict()
        result['meta'] = meta
        result['entity'] = entity
        result['data'] = data
        return result


# classifications are education/ business/ location
# entity: the entity of that classification
# search a entity with classification
# -- type
class Entity:
    def __init__(self, classification, _id='', name='', ip='127.0.0.1', port=27017):
        assert classification in ['business', 'employments', 'locations', 'educations'], \
            ('API_ERROR' + '@' + 'Entity: ' +
             'The <classification> parameter has error in the query.')

        assert (_id is not '') or (name is not ''), ('API_ERROR' + '@' + 'Entity: '
                                         + 'The <id> or <name> parameter has error in the query.')

        self.classification = classification
        self.id = _id
        self.name = name

        self.entity = {}

        self.client = MongoClient(ip, port)
        self.query()
        self.client.close()

    def query(self):
        db = self.client.zhihu

        if self.id:
            self.entity = db[self.classification].find_one({'_id': self.id})
        elif self.name:
            pattern = r'.*' + self.name + r'.*'
            value = re.compile(pattern)
            self.entity = db[self.classification].find_one({'name': value})

        meta = {
            'query_type': 'Entity',
            'database': 'zhihu',
            'classification': self.classification,
            'id': self.id,
            'name': self.name
        }
        data = self.entity
        result = OrderedDict()
        result['meta'] = meta
        result['data'] = data
        return result


# person: query a person, with his/her followers & followees
# -- person
class Person:
    def __init__(self, id, ip='127.0.0.1', port=27017):
        pattern = r'^[-\w]+$'
        valid = re.compile(pattern)
        assert valid.match(id), ('API_ERROR' + '@' +
                                 'Person: The <id> parameter has error in the query.')

        self.id = id
        self.person = {}
        self.followers = []
        self.followees = []

        self.client = MongoClient(ip, port)
        self.query()
        self.client.close()

    def query(self):
        db = self.client.zhihu
        self.person = db.users.find_one({'_id': self.id})
        if self.person:
            followers_query = db.followers.find_one({'_id': self.id})
            if followers_query:
                self.followers = followers_query['value']['data']

            followees_query = db.followees.find_one({'_id': self.id})
            if followees_query:
                self.followees = followees_query['value']['data']
        meta = {
            'query_type': 'Person',
            'database': 'zhihu',
            'id': self.id,
        }
        person = self.person
        data = copy.deepcopy(self.person)
        data['followers'] = self.followers
        data['followees'] = self.followees
        result = OrderedDict()
        result['meta'] = meta
        result['person'] = person
        result['data'] = data
        return result


# person: query a person
# -- simple-person
class SimplePerson:
    def __init__(self, id, ip='127.0.0.1', port=27017):
        pattern = r'^[-\w]+$'
        valid = re.compile(pattern)
        assert valid.match(id), ('API_ERROR' + '@' +
                                 'SimplePerson: The <id> parameter has error in the query.')
        self.id = id
        self.person = {}

        self.client = MongoClient(ip, port)
        self.query()
        self.client.close()

    def query(self):
        db = self.client.zhihu
        self.person = db.users.find_one({'_id': self.id})
        meta = {
            'query_type': 'SimplePerson',
            'database': 'zhihu',
            'id': self.id,
        }
        data = self.person
        result = OrderedDict()
        result['meta'] = meta
        result['data'] = data
        return result


# classifications are education/ business/ location
# entity: the entity of that classification
# search a top entity with most people
# -- top_type
class TopEntityByPersonNumber:
    def __init__(self, classification, limit=20, ip='127.0.0.1', port=27017):
        assert classification in ['business', 'employments', 'locations', 'educations'], \
            ('API_ERROR' + '@' + 'TopEntityByPersonNumber: ' +
             'The <classification> parameter has error in the query.')

        self.classification = classification
        self.limit = limit
        self.top = []

        self.client = MongoClient(ip, port)
        self.query()
        self.client.close()

    def query(self):
        db = self.client.zhihu
        pipeline = [
            {'$sort': SON([('num', -1)])},
            {'$limit': self.limit}
        ]
        self.top = list(db[self.classification].aggregate(pipeline))
        meta = {
            'query_type': 'TopEntityByPersonNumber',
            'database': 'zhihu',
            'classification': self.classification,
            'limit': self.limit
        }
        data = self.top
        result = OrderedDict()
        result['meta'] = meta
        result['data'] = data
        return result


# search top persons by the value
# -- top_person
class TopPersonByValue:
    def __init__(self, value, limit=20, ip='127.0.0.1', port=27017, **kwargs):
        value_list = ["answer_count", "articles_count", "columns_count",
                      "question_count", "following_count", "follower_count",
                      "logs_count", "favorite_count", "participated_live_count",
                      "hosted_live_count", "following_question_count", "following_topic_count",
                      "voteup_count", "favorited_count", "thanked_count", "following_favlists_count"]
        assert value in value_list, \
            ('API_ERROR' + '@' + 'TopPersonByValue: ' +
             'The <value> parameter has error in the query.')

        self.value = value

        self.limit = limit
        self.kwargs = kwargs

        self.client = MongoClient(ip, port)
        self.query()
        self.client.close()

    def query(self):
        db = self.client.zhihu
        match = {}
        for k, v in self.kwargs.items():
            match[k] = int(v)
        pipeline = [
            {'$sort': SON([(self.value, -1)])},
            {'$match': match},
            {'$limit': int(self.limit)},
        ]
        mylog.warning(pipeline)

        self.top = list(db.users.aggregate(pipeline))
        mylog.warning(self.top)

        meta = {
            'query_type': 'TopPersonByValue',
            'value': self.value,
            'limit': self.limit,
            'kwargs': self.kwargs,
        }
        data = self.top
        result = OrderedDict()
        result['meta'] = meta
        result['data'] = data
        return result


