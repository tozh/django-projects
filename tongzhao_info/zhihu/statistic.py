from pymongo import MongoClient
from bson.son import SON


ip='127.0.0.1'
port=27017

client = MongoClient(ip, port)
db = client.zhihu


def class_sum(db):
    classification = [ "gender", "is_org", "is_advertiser"]
    accumulator = ["sum", ]

    for c in classification:
            for a in accumulator:
                pipeline = [
                    {'$group': {'_id':'$'+c, c:{'$'+a: 1}}},
                    {"$sort": SON([(c, -1)])},
                    {'$out': c+'_'+a}
                ]
                db.users.aggregate(pipeline)


def class_avg_and_max_value(db):
    classification = ["gender", "business", "is_org", "is_advertiser"]

    classification_array = ["employments", "locations", "educations", ]
    value = ["answer_count", "articles_count", "columns_count",
             "question_count", "following_count", "follower_count",
             "logs_count", "favorite_count", "participated_live_count",
             "hosted_live_count", "following_question_count", "following_topic_count",
             "voteup_count", "favorited_count", "thanked_count", "following_favlists_count"]

    accumulator = ["avg", "max"]

    for c in classification:
        for v in value:
            for a in accumulator:
                pipeline = [
                    {'$group':{'_id':'$'+c, v:{'$'+a:'$'+v}}},
                    {'$sort': SON([(v, -1)])},
                    {'$out': '_'+c+'_'+a+'_'+v}
                ]
                db.users.aggregate(pipeline)

    for c in classification_array:
        for v in value:
            for a in accumulator:
                pipeline = [
                    {'$unwind': '$'+c},
                    {'$group':{'_id':'$'+c, v:{'$'+a:'$'+v}}},
                    {'$sort': SON([(v, -1)])},
                    {'$out': '_'+c+'_'+a+'_'+v}
                ]
                db.users.aggregate(pipeline)


def top100_value(db):
    value = ["answer_count", "articles_count", "columns_count",
             "question_count", "following_count", "follower_count",
             "logs_count", "favorite_count", "participated_live_count",
             "hosted_live_count", "following_question_count", "following_topic_count",
             "voteup_count", "favorited_count", "thanked_count",
             "following_favlists_count"]

    for v in value:
        pipeline = [
            {'$project': {'name':1, 'gender':1, v:1, 'is_org':1, 'is_advertiser':1, 'is_bind_sina':1}},
            {'$sort': SON([(v, -1)])},
            {'$limit': 100},
            {'$out': '_'+'top100_'+v}
        ]
        db.users.aggregate(pipeline)

# def gender_top100_value(db):
#     value = ["answer_count", "articles_count", "columns_count",
#              "question_count", "following_count", "follower_count",
#              "logs_count", "favorite_count", "participated_live_count",
#              "hosted_live_count", "following_question_count", "following_topic_count",
#              "voteup_count", "favorited_count", "thanked_count",
#              "following_favlists_count"]
#
#     for v in value:
#         pipeline = [
#             {'$project': {'name': 1, 'gender': 1, v: 1, 'is_org': 1, 'is_advertiser': 1, 'is_bind_sina': 1}},
#             {'$sort': SON([(v, -1)])},
#             {'$limit': 100},
#             {'$out': '_' + 'top100_' + v}
#         ]
#         db.users.aggregate(pipeline)


# class_sum(db)
top100_value(db)
class_avg_and_max_value(db)






