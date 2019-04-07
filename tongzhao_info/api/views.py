from django.shortcuts import render
from django.http import HttpResponse

# from zhihu import Person, Type, TopType, TopPerson, TypeTopPerson
#
# import re
# import json
#
# MONGODB_IP = '127.0.0.1'
# MONGODB_PORT = 27017
#
#
# # Create your views here.
# def person_search(request):
#     if request.method=='GET':
#         req = request.GET
#     elif request.method=='POST':
#         req = request.POST
#     else:
#         res = json.dumps({'error':'Your API is invalid!', 'error_type': 'api_error'})
#         return HttpResponse(content=res, content_type='application/json', status=400)
#
#     if 'id' in req:
#         pattern = r'^[-\w]+$'
#         valid = re.compile(pattern)
#         id = req['id']
#         if valid.match(id):
#             p = Person(id)
#             p_dict = p.to_dict()
#             if 'data' in p_dict and p_dict['data']:
#                 res = json.dumps(p_dict)
#                 return HttpResponse(content=res, content_type='application/json', status=200)
#             else:
#                 res = json.dumps({'error': 'Cannot find the id in the Database!'
#                                      , 'error_type': 'not_found'})
#                 return HttpResponse(content=res, content_type='application/json', status=404)
#         else:
#             res = json.dumps({'error':'The ID is invalid!', 'error_type': 'id_error'})
#             return HttpResponse(content=res, content_type='application/json', status=400)
#     else:
#         res = json.dumps({'error': 'Your API is invalid!', 'error_type': 'api_error'})
#         return HttpResponse(content=res, content_type='application/json', status=400)
#
#
# def type_search(request):
#     if request.method == 'GET':
#         req = request.GET
#     elif request.method == 'POST':
#         req = request.POST
#     else:
#         res = json.dumps({'error': 'Your API is invalid!', 'error_type': 'api_error'})
#         return HttpResponse(content=res, content_type='application/json', status=400)
#
#     type = req['type'] if 'type' in req else ''
#     id = req['id'] if 'id' in req else ''
#     name = req['name'] if 'name' in req else ''
#     t = Type(type, id, name)
#     t_dict = t.to_dict()
#     res = json.dumps(t_dict)
#     return HttpResponse(content=res, content_type='application/json', status=200)
#
#
# def type_top_person(request):
#     if request.method == 'GET':
#         req = request.GET
#     elif request.method == 'POST':
#         req = request.POST
#     else:
#         res = json.dumps({'error': 'Your API is invalid!', 'error_type': 'api_error'})
#         return HttpResponse(content=res, content_type='application/json', status=400)
#
#     type = req['type'] if 'type' in req else ''
#     sort = req['sort'] if 'sort' in req else ''
#     id = req['id'] if 'id' in req else ''
#     name = req['name'] if 'name' in req else ''
#     kwargs = {'gender':req['gender']} if 'gender' in req else {}
#
#     ttp = TypeTopPerson(type, sort, id, name, **kwargs)
#     ttp_dict = ttp.to_dict()
#     res = json.dumps(ttp_dict)
#     return HttpResponse(content=res, content_type='application/json', status=200)
#
#
# def top_type(request):
#     if request.method == 'GET':
#         req = request.GET
#     elif request.method == 'POST':
#         req = request.POST
#     else:
#         res = json.dumps({'error': 'Your API is invalid!', 'error_type': 'api_error'})
#         return HttpResponse(content=res, content_type='application/json', status=400)
#
#     type = req['type'] if 'type' in req else ''
#     tt = TopType(type)
#     tt_dict = tt.to_dict()
#     res = json.dumps(tt_dict)
#     return HttpResponse(content=res, content_type='application/json', status=200)
#
#
# def top_person(request):
#     if request.method == 'GET':
#         req = request.GET
#     elif request.method == 'POST':
#         req = request.POST
#     else:
#         res = json.dumps({'error': 'Your API is invalid!', 'error_type': 'api_error'})
#         return HttpResponse(content=res, content_type='application/json', status=400)
#
#     sort = req['sort'] if 'sort' in req else ''
#     kwargs = {k: v for k, v in req.items() if k!='sort'}
#     tp = Type(sort, **kwargs)
#     tp_dict = tp.to_dict()
#     res = json.dumps(tp_dict)
#     return HttpResponse(content=res, content_type='application/json', status=200)



