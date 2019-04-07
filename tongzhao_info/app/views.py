from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template import loader, Context
from app.models import CustomUser
from app.models import BlogArticle
from app.models import BlogCategory
from app.models import BlogComment
from app.models import BlogTag
from app.models import UserTag
from app.models import TaggingBlog
from app.models import LikeBlog
from app.models import LikeComment
from app.models import ClickBlog

from app.serializers import CustomUserSerializer
from app.serializers import BlogCategorySerializer
from app.serializers import BlogArticleSerializer
from app.serializers import BlogTagSerializer
from app.serializers import UserTagSerializer
from app.serializers import TaggingBlogSerializer
from app.serializers import LikeBlogSerializer
from app.serializers import LikeCommentSerializer
from app.serializers import ClickBlogSerializer
from app.serializers import BlogCommentSerializer

from rest_framework.settings import api_settings
from rest_framework.decorators import permission_classes
from app.permissions import CustomUserPermission
from app.permissions import BlogArticlePermission
from app.permissions import BlogCategoryPermission
from app.permissions import BlogCommentPermission

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import AllowAny

from rest_framework.decorators import detail_route, list_route

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import logging

mylog = logging.getLogger(__name__)

# Create your views here.

def app_index(request):
    t = loader.get_template('index.html')
    return HttpResponse(t.render())


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.filter()
    lookup_field = 'username'
    permission_classes = (CustomUserPermission,)

    # @permission_classes((AllowAny, ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        queryset = CustomUser.objects.filter(username=serializer.data['username'])
        user = get_object_or_404(queryset)
        default_category = BlogCategory.objects.create(
            name='Default Category',
            user=user,
            is_deletable=False)
        default_category.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # @permission_classes((IsAdminUser, ))
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # @permission_classes((AllowAny, ))
    # def retrieve(self, request, *args, **kwargs):
    #     mylog.warning('+++++++++++++++++++++++++++++++')
    #     instance = self.get_object()
    #     self.check_object_permissions(request, instance)
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # @permission_classes((AllowSelf, ))
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data)

    # @permission_classes((NotAllow, ))
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['GET'])
    # @permission_classes((IsAuthenticated,))
    def list_articles(self, request, pk=None):
        user = request.user
        queryset = BlogArticle.objects.filter(author=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        for blog_data in serializer.data:
            if user.is_authenticated:
                try:
                    blog = BlogArticle.objects.get(id=blog_data['id'])
                    blog_data['is_liked'] = True if self.is_liked(user=user, blog=blog) else False
                except BlogArticle.DoesNotExist:
                    blog_data['is_liked'] = False
            else:
                blog_data['is_liked'] = False

            if blog_data['author'] == user.username:
                blog_data['is_owner'] = True
            else:
                blog_data['is_owner'] = False
        return Response(serializer.data)

    # @detail_route(methods=['GET'])
    # @permission_classes((IsAuthenticated,))
    # def list_categories(self, request, pk=None):
    #     user = request.user
    #     mylog.warning(type(pk))
    #     mylog.warning(pk)
    #     queryset = BlogCategory.objects.filter(user=pk)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(queryset, many=True)
    #     if user.username == pk:
    #         for category_data in serializer.data:
    #                 category_data['is_owner'] = True
    #     else:
    #         for category_data in serializer.data:
    #             category_data['is_owner'] = False
    #     return Response(serializer.data)

    def is_liked(self, user, blog):
        like_blog = LikeBlog.objects.filter(user=user, blog=blog)
        return True if like_blog else False


class BlogArticleViewSet(viewsets.ModelViewSet):
    serializer_class = BlogArticleSerializer
    queryset = BlogArticle.objects.filter(is_active=True)
    lookup_field = 'id'
    permission_classes = (BlogArticlePermission, )

    # @permission_classes((IsAuthenticated, ))
    def create(self, request, *args, **kwargs):
        user = request.user
        mylog.warning(user)
        request.data['author'] = user
        if not ('category' in request.data and request.data['category']):
            queryset = BlogCategory.objects.filter(name='Default Category', user=user)
            mylog.warning(queryset)
            category = get_object_or_404(queryset)
            request.data['category'] = category

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # @permission_classes((AllowAny,))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance['click_count'] += 1
        user = request.user
        kwargs = {'user': user, 'blog': instance}
        click_blog = ClickBlog.objects.create(**kwargs)
        click_blog.save()
        serializer = self.get_serializer(instance)
        response = serializer.data
        if user.is_authenticated:
            response['is_liked'] = self.is_liked(user, instance)
            if user.username == instance['author']:
                response['is_owner'] = True
            else:
                response['is_owner'] = False
        else:
            response['is_liked'] = False
            response['is_owner'] = False
        instance.save()
        return Response(response)

    def is_liked(self, user, blog):
        like_blog = LikeBlog.objects.filter(user=user, blog=blog)
        return True if like_blog else False

    # @permission_classes((AllowOwner,))
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data)

    # @permission_classes((IsAdminUser,))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        user = request.user
        mylog.warning('-----------------------')
        mylog.warning(user.is_authenticated)
        for blog_data in serializer.data:
            if user.is_authenticated:
                try:
                    blog = BlogArticle.objects.get(id=blog_data['id'])
                    blog_data['is_liked'] = True if self.is_liked(user=user, blog=blog) else False
                except BlogArticle.DoesNotExist:
                    blog_data['is_liked'] = False
            else:
                blog_data['is_liked'] = False

            if blog_data['author'] == user.username:
                blog_data['is_owner'] = True
            else:
                blog_data['is_owner'] = False
        return Response(serializer.data)

    @detail_route(methods=['POST', 'PATCH'])
    # @permission_classes((AllowOwner,))
    def inactive(self, request, pk=None):
        queryset = BlogArticle.objects.filter(id=pk)
        instance = get_object_or_404(queryset)
        self.check_object_permissions(self.request, instance)

        mylog.warning(instance.title)
        instance.is_active = request['is_active']
        instance.save()
        return_data = {
            "blog": instance.id,
            "is_active": instance.is_active,
            "inactive": "success"}
        return Response(data=return_data, status=status.HTTP_202_ACCEPTED)


class BlogCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.filter()
    lookup_field = 'id'
    permission_classes = (BlogCategoryPermission, )

    # @permission_classes((IsAuthenticated,))
    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # @permission_classes((AllowAny,))
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # @permission_classes((AllowOwner,))
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data)

    # @permission_classes((AllowOwner,))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance['is_deletable']:
            user = request.user
            queryset = BlogCategory.objects.filter(name='Default Category', user=user)
            category = get_object_or_404(queryset)
            for blog in instance.blog_set:
                category.blog_set.add(blog)
            category.save()

            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # @permission_classes((IsAdminUser,))
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


class BlogTagViewSet(viewsets.ModelViewSet):
    serializer_class = BlogTagSerializer
    queryset = BlogTag.objects.filter()
    lookup_field = 'name'


class TaggingBlogViewSet(viewsets.ModelViewSet):
    serializer_class = TaggingBlogSerializer
    queryset = TaggingBlog.objects.filter()
    lookup_field = 'id'


class UserTagViewSet(viewsets.ModelViewSet):
    serializer_class = UserTagSerializer
    queryset = UserTag.objects.filter()
    lookup_field = 'id'


class BlogCommentViewSet(viewsets.ModelViewSet):
    serializer_class = BlogCommentSerializer
    queryset = BlogComment.objects.filter()
    lookup_field = 'id'
    permission_classes = (BlogCommentPermission, )

    # @permission_classes((IsAuthenticated,))
    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # @permission_classes((AllowAny,))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance)
        response = serializer.data
        if user.is_authenticated:
            response['is_liked'] = self.is_liked(user, instance)
            if user.username == instance['user']:
                response['is_owner'] = True
            else:
                response['is_owner'] = False
        else:
            response['is_liked'] = False
            response['is_owner'] = False
        instance.save()
        return Response(response)

    def is_liked(self, user, comment):
        like_comment = LikeComment.objects.filter(user=user, comment=comment)
        return True if like_comment else False

    # @permission_classes((IsAuthenticated, ))
    def list(self, request, *args, **kwargs):
        if 'comment' in request:
            try:
                comment = BlogComment.objects.get(id=request.data['comment'])
                queryset = BlogComment.objects.filter(response_to=comment)

            except BlogComment.DoesNotExist:
                response = {'type': 'comment', 'comment': request.data['comment'], 'error': 'No comments yet.'}
                return Response(response)
        elif 'blog' in request.data:
            try:
                blog = BlogArticle.objects.get(id=request.data['blog'])
                queryset = BlogComment.objects.filter(blog=blog)

            except BlogArticle.DoesNotExist:
                response = {'type':'blog', 'blog': request.data['blog'], 'error':'No comments yet.'}
                return Response(response)
        else:
            queryset = BlogComment.objects.none()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        user = request.user
        for comment_data in serializer.data:
            if user.is_authenticated:
                try:
                    comment = BlogComment.objects.get(id=comment_data['id'])
                    comment_data['is_liked'] = True if self.is_liked(user=user, comment=comment) else False
                except BlogArticle.DoesNotExist:
                    comment_data['is_liked'] = False

                if user.username == comment_data['user']:
                    comment_data['is_owner'] = True
                else:
                    comment_data['is_owner'] = False
            else:
                comment_data['is_liked'] = False
                comment_data['is_owner'] = False
        return Response(serializer.data)

    # @permission_classes((NotAllow,))
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # @permission_classes((NotAllow,))
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data)

    @detail_route(methods=['POST', 'PATCH'])
    # @permission_classes((AllowOwner,))
    def inactive(self, request, pk=None):
        queryset = BlogComment.objects.filter(id=pk)
        instance = get_object_or_404(queryset)
        self.check_object_permissions(self.request, instance)
        instance.is_active = request['is_active']
        instance.save()
        return_data = {
            "comment": instance.id,
            "is_active": instance.is_active,
            "inactive": "success"}

        return Response(data=return_data, status=status.HTTP_202_ACCEPTED)


class LikeBlogViewSet(viewsets.ModelViewSet):
    serializer_class = LikeBlogSerializer
    queryset = LikeBlog.objects.filter()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        if request.data['user'] == request.user and 'blog' in request.data:
            blog = request.data['blog']
            blog.like_count -= 1
            blog.save()

            queryset = LikeBlog.objects.filter(user=request.user, blog=blog)
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = {'error': 'API format error.'}
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class LikeCommentViewSet(viewsets.ModelViewSet):
    serializer_class = LikeCommentSerializer
    queryset = LikeComment.objects.filter()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        if request.data['user'] == request.user and 'comment' in request.data:
            comment = request.data['comment']
            comment.like_count -= 1
            comment.save()

            queryset = LikeBlog.objects.filter(user=request.user, comment=comment)
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = {'error': 'API format error.'}
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class ClickBlogViewSet(viewsets.ModelViewSet):
    serializer_class = ClickBlogSerializer
    queryset = ClickBlog.objects.filter()
    lookup_field = 'id'



