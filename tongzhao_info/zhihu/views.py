from django.shortcuts import render
from django.http import HttpResponse
from zhihu import Person
from zhihu import SimplePerson
from zhihu import Entity
from zhihu import TopPersonByValue
from zhihu import TopPersonOfEntity
from zhihu import TopEntityByPersonNumber
from zhihu import StatisticQuery

import re
import json

MONGODB_IP = '127.0.0.1'
MONGODB_PORT = 27017

import logging
mylog = logging.getLogger(__name__)


# Create your views here.
def person(request):
    try:
        assert request.method == 'GET', ('METHOD_ERROR' + '@' + 'view.person: ' +
                                         'The <request.method> should be \'GET\'.')
        req = request.GET

        assert 'id' in req, ('API_ERROR' + '@' + 'view.person: ' +
                             'The <id> parameter has error in the query.')
        id = req['id']
        result = Person(id).query()

        assert 'data' in result and result['data'], ('NOT_FOUND_ERROR' + '@' + 'view.person: ' +
                                                     'Cannot found the <id> in database.')

        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=200)
    except AssertionError as e:
        error_str_list = e.__str__().split('@')
        error_type = error_str_list[0]
        error_message = error_str_list[1]
        error = {
            'error_type': error_type,
            'error_message': error_message
        }
        result = {
            'error': error
        }
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=400)


def simple_person(request):
    try:
        assert request.method == 'GET', ('METHOD_ERROR' + '@' + 'view.simple_person: ' +
                                         'The <request.method> should be \'GET\'.')
        req = request.GET

        assert 'id' in req, ('API_ERROR' + '@' + 'view.simple_person: ' +
                             'The <id> parameter has error in the query.')
        id = req['id']
        result = SimplePerson(id).query()

        assert 'data' in result and result['data'], ('NOT_FOUND_ERROR' + '@' + 'view.simple_person: ' +
                                                     'Cannot found the data in database.')

        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=200)
    except AssertionError as e:
        error_str_list = e.__str__().split('@')
        error_type = error_str_list[0]
        error_message = error_str_list[1]
        error = {
            'error_type': error_type,
            'error_message': error_message
        }
        result = {
            'error': error
        }
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=400)



def entity(request):
    try:
        assert request.method == 'GET', ('METHOD_ERROR' + '@' + 'view.entity: ' +
                                         'The <request.method> should be \'GET\'.')
        req = request.GET

        assert 'classification' in req, ('API_ERROR' + '@' + 'view.entity: ' +
                                         'The <classification> parameter has error in the query.')

        classification = req['classification']

        assert 'id' in req or 'name' in req, ('API_ERROR' + '@' + 'view.entity: ' +
                                              'The <id> or <name> parameter has error in the query.')

        id = req['id'] if 'id' in req else ''
        name = req['name'] if 'name' in req else ''
        result = Entity(classification, id, name).query()

        assert 'data' in result and result['data'], ('NOT_FOUND_ERROR' + '@' + 'view.simple_person: ' +
                                                     'Cannot found the data in database.')
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=200)
    except AssertionError as e:
        error_str_list = e.__str__().split('@')
        error_type = error_str_list[0]
        error_message = error_str_list[1]
        error = {
            'error_type': error_type,
            'error_message': error_message
        }
        result = {
            'error': error
        }
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=400)


def top_person_of_entity(request):
    try:
        assert request.method == 'GET', ('METHOD_ERROR' + '@' + 'view.top_person_of_entity: ' +
                                         'The <request.method> should be \'GET\'.')
        req = request.GET

        assert 'classification' in req, ('API_ERROR' + '@' + 'view.top_person_of_entity: ' +
                                         'The <classification> parameter has error in the query.')

        assert 'value' in req, ('API_ERROR' + '@' + 'view.top_person_of_entity: ' +
                                'The <value> parameter has error in the query.')

        classification = req['classification']
        value = req['value']
        limit = int(req['limit']) if 'limit' in req else 20

        assert 'id' in req or 'name' in req, ('API_ERROR' + '@' + 'view.entity: ' +
                                              'The <id> or <name> parameter has error in the query.')
        id = req['id'] if 'id' in req else ''
        name = req['name'] if 'name' in req else ''
        if 'gender' in req and (int(req['gender']) == 0 or int(req['gender']) == 1):
            kwargs = {'gender': int(req['gender'])}
        else:
            kwargs =  {}

        result = TopPersonOfEntity(classification, value, id, name, limit, **kwargs).query()

        assert 'data' in result and result['data'], ('NOT_FOUND_ERROR' + '@' + 'view.top_person_of_entity: ' +
                                                     'Cannot found the data in database.')
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=200)

    except AssertionError as e:
        error_str_list = e.__str__().split('@')
        error_type = error_str_list[0]
        error_message = error_str_list[1]
        error = {
            'error_type': error_type,
            'error_message': error_message
        }
        result = {
            'error': error
        }
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=400)


def top_entity_by_person_number(request):
    try:
        assert request.method == 'GET', ('METHOD_ERROR' + '@' + 'view.entity: ' +
                                         'The <request.method> should be \'GET\'.')
        req = request.GET

        assert 'classification' in req, ('API_ERROR' + '@' + 'view.top_entity_by_person_number: ' +
                                'The <classification> parameter has error in the query.')

        classification = req['classification']
        limit = int(req['limit']) if 'limit' in req else 20
        result = TopEntityByPersonNumber(classification, limit).query()

        assert 'data' in result and result['data'], ('NOT_FOUND_ERROR' + '@' + 'view.top_person_by_value: ' +
                                                     'Cannot found the data in database.')
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=200)

    except AssertionError as e:
        error_str_list = e.__str__().split('@')
        error_type = error_str_list[0]
        error_message = error_str_list[1]
        error = {
            'error_type': error_type,
            'error_message': error_message
        }
        result = {
            'error': error
        }
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=400)


def top_person_by_value(request):
    try:
        assert request.method == 'GET', ('METHOD_ERROR' + '@' + 'view.entity: ' +
                                         'The <request.method> should be \'GET\'.')
        req = request.GET

        assert 'value' in req, ('API_ERROR' + '@' + 'view.top_person_by_value: ' +
                                'The <value> parameter has error in the query.')

        value = req['value'] if 'value' in req else ''
        kwargs = {k: v for k, v in req.items() if k != 'value'}
        mylog.warning(kwargs)
        result = TopPersonByValue(value, **kwargs).query()

        assert 'data' in result and result['data'], ('NOT_FOUND_ERROR' + '@' + 'view.top_person_by_value: ' +
                                                     'Cannot found the <id> in database.')
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=200)

    except AssertionError as e:
        error_str_list = e.__str__().split('@')
        error_type = error_str_list[0]
        error_message = error_str_list[1]
        error = {
            'error_type': error_type,
            'error_message': error_message
        }
        result = {
            'error': error
        }
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=400)


def statistic(request):
    try:
        assert request.method == 'GET', ('METHOD_ERROR' + '@' + 'view.entity: ' +
                                         'The <request.method> should be \'GET\'.')
        req = request.GET
        kwargs = req
        # accumulator = kwargs['accumulator'] if 'accumulator' in kwargs else ''
        # cls = kwargs['classification'] if 'classification' in kwargs else ''
        # value = kwargs['value'] if 'value' in kwargs else ''
        result = StatisticQuery().query()
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=200)
    except AssertionError as e:
        error_str_list = e.__str__().split('@')
        error_type = error_str_list[0]
        error_message = error_str_list[1]
        error = {
            'error_type': error_type,
            'error_message': error_message
        }
        result = {
            'error': error
        }
        res = json.dumps(result)
        return HttpResponse(content=res, content_type='application/json', status=400)







