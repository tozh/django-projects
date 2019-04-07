from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.permissions import BasePermission
import logging

mylog = logging.getLogger(__name__)


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class AllowOwner(IsAuthenticated, DjangoObjectPermissions):
    def has_object_permission(self, request, view, obj):
        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user
        if model_cls.__name__ == 'BlogArticle':
            assert hasattr(obj, 'author') \
                   or getattr(obj, 'author', None) is not None, (
                'Cannot apply AllowOwner on a obj that does not have attribute [author]')
            return user.is_authenticated and user.username == obj.author.username
        else:
            assert hasattr(obj, 'user') \
                   or getattr(obj, 'user', None) is not None, (
                'Cannot apply AllowOwner on a obj that does not have attribute [user]')

            return user.is_authenticated and user.username == obj.user.username


class AllowSelf(IsAuthenticated, DjangoObjectPermissions):
    def has_object_permission(self, request, view, obj):
        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user

        if model_cls.__name__ == 'CustomUser':
            assert hasattr(obj, 'username') \
                   or getattr(obj, 'username', None) is not None, (
                'Cannot apply AllowSelf on a obj that does not have attribute [username]')
            return user.is_authenticated and user.username == obj.username
        else:
            return False


class NotAllow:

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class CustomUserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            permission_cls = AllowAny()
            return permission_cls.has_permission(request=request, view=view)
        elif view.action == 'list':
            permission_cls = IsAdminUser()
            return permission_cls.has_permission(request=request, view=view)
        elif view.action == 'list_articles':
            permission_cls = IsAuthenticated()
            return permission_cls.has_permission(request=request, view=view)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            permission_cls = NotAllow()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'update':
            permission_cls = AllowSelf()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'retrieve':
            permission_cls = AllowAny()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        else:
            return True


class BlogArticlePermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            permission_cls = IsAuthenticated()
            return permission_cls.has_permission(request=request, view=view)
        elif view.action == 'list':
            permission_cls = IsAdminUser()
            return permission_cls.has_permission(request=request, view=view)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            permission_cls = NotAllow()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'update':
            permission_cls = AllowOwner()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'retrieve':
            permission_cls = AllowAny()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'inactive':
            permission_cls = AllowOwner()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        else:
            return False


class BlogCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            permission_cls = IsAuthenticated()
            return permission_cls.has_permission(request=request, view=view)
        elif view.action == 'list':
            permission_cls = IsAdminUser()
            return permission_cls.has_permission(request=request, view=view)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            permission_cls = NotAllow()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'update':
            permission_cls = AllowOwner()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'retrieve':
            permission_cls = AllowAny()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        else:
            return False


class BlogCommentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            permission_cls = IsAuthenticated()
            return permission_cls.has_permission(request=request, view=view)
        elif view.action == 'list':
            permission_cls = AllowAny()
            return permission_cls.has_permission(request=request, view=view)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            permission_cls = NotAllow()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'update':
            permission_cls = NotAllow()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'retrieve':
            permission_cls = AllowAny()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        elif view.action == 'inactive':
            permission_cls = AllowOwner()
            return permission_cls.has_object_permission(request=request, view=view, obj=obj)
        else:
            return False

