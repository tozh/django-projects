from pymongo import MongoClient
from collections import OrderedDict
import re
from bson.son import SON


class StatisticQuery:
    def __init__(self, limit=50, ip='127.0.0.1', port=27017, **kwargs):
        self.accumulator = kwargs['accumulator'] if 'accumulator' in kwargs else ''
        self.cls = kwargs['classification'] if 'classification' in kwargs else ''
        self.value = kwargs['value'] if 'value' in kwargs else ''
        self.limit = limit
        if self.limit > 100:
            self.limit = 100
        self.ip = ip
        self.port = port

    def query(self):
        client = MongoClient(self.ip, self.port)
        value_list = ["answer_count", "articles_count", "columns_count",
                 "question_count", "following_count", "follower_count",
                 "logs_count", "favorite_count", "participated_live_count",
                 "hosted_live_count", "following_question_count", "following_topic_count",
                 "voteup_count", "favorited_count", "thanked_count",
                 "following_favlists_count"]

        if self.accumulator == 'sum':
            assert self.cls in ["gender", "is_org", "is_advertiser"], \
                ('API_ERROR' + '@' + 'StatisticQuery: The <classification>' +
                 'parameter has error in the sum query.')
            collection = self.cls+'_sum'
            client.close()
            return self.query_class_sum(client, collection)
        elif self.accumulator == 'avg' or self.accumulator == 'max':
            cls_list = ["gender", "business", "is_org", "is_advertiser", "employments", "locations", "educations"]

            assert self.cls in cls_list, ('API_ERROR@StatisticQuery: The <classification> parameter has error in the'
                                          + self.accumulator + 'query.')
            assert self.value in value_list, ('API_ERROR@StatisticQuery: The <value> parameter has error in the'
                                          + self.accumulator + 'query.')

            collection = '_' + self.cls + '_' + self.accumulator + '_' + self.value
            client.close()
            return self.query_class_avg_or_max_value(client, collection)
        elif self.accumulator == 'top':
            assert self.value in value_list, ('API_ERROR@StatisticQuery: The <value> parameter has error in the'
                                              + self.accumulator + 'query.')
            collection = '_' + self.accumulator + '100_' + self.value
            client.close()
            return self.query_top100_value(client, collection)

        else:
            meta = {
            'query_type': 'StatisticQuery',
            'database': 'zhihu',
            'accumulator': self.accumulator,
            'classification': self.cls,
            'value': self.value,
            'collection': '',
            'limit': self.limit,
            }
            data = []
            result = OrderedDict()
            result['meta'] = meta
            result['data'] = data
            result['error'] = {
                'error_type': 'API_ERROR',
                'error_message': 'StatisticQuery: The <accumulator> parameter has error in the query'
            }
            return result

    def query_class_sum(self, client, collection):
        db = client.zhihu
        col = db[collection]
        meta = {
            'query_type': 'StatisticQuery',
            'database': 'zhihu',
            'accumulator': self.accumulator,
            'classification': self.cls,
            'value': self.value,
            'collection': collection,
            'limit': self.limit,

        }
        data = list(col.find().sort(SON([('_id', -1)])))
        result = OrderedDict()
        result['meta'] = meta
        result['data'] = data
        return result

    def query_class_avg_or_max_value(self, client, collection):
        db = client.zhihu
        col = db[collection]
        meta = {
            'query_type': 'StatisticQuery',
            'database': 'zhihu',
            'accumulator': self.accumulator,
            'classification': self.cls,
            'value': self.value,
            'collection': collection,
            'limit': self.limit,

        }
        data = list(col.find().sort(SON([(self.value, -1)])).limit(self.limit))
        result = OrderedDict()
        result['meta'] = meta
        result['data'] = data
        return result

    def query_top100_value(self, client, collection):
        db = client.zhihu
        col = db[collection]
        meta = {
            'query_type': 'StatisticQuery',
            'database': 'zhihu',
            'accumulator': self.accumulator,
            'classification': self.cls,
            'value': self.value,
            'collection': collection,
            'limit': self.limit,
        }
        data = list(col.find().sort(SON([(self.value, -1)])).limit(self.limit))
        result = OrderedDict()
        result['meta'] = meta
        result['data'] = data
        return result








