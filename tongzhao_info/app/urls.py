from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from app.views import CustomUserViewSet
from app.views import BlogCategoryViewSet
from app.views import BlogArticleViewSet
from app.views import BlogTagViewSet
# from app.views import BlogTagSetViewSet
from app.views import TaggingBlogViewSet
from app.views import BlogCommentViewSet
from app.views import LikeBlogViewSet
from app.views import LikeCommentViewSet



from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

router = DefaultRouter()
router.register('user', CustomUserViewSet, base_name='user')
router.register('blog', BlogArticleViewSet, base_name='blog')
router.register('category', BlogCategoryViewSet, base_name='category')
router.register('tag', BlogTagViewSet, base_name='tag')
# router.register('tag_set', BlogTagSetViewSet, base_name='tag_set')
router.register('tagging_blog', TaggingBlogViewSet, base_name='tagging_blog')
router.register('comment', BlogCommentViewSet, base_name='comment')
router.register('like_blog', LikeBlogViewSet, base_name='like_blog')
router.register('like_comment', LikeCommentViewSet, base_name='like_comment')


other_urlpatterns = [
    path('', views.app_index, name='app-index'),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
]

urlpatterns = other_urlpatterns + router.urls
