from rest_framework import serializers
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


from django.utils import timezone
import re


import logging

mylog = logging.getLogger(__name__)


class SimpleBlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = (
            'id',
            'content',
            'created_time',
            'like_count',
            'blog',
            'user',
            'serial_num',
            'is_active',
            'response_to',
            'response_serial_num',
            'response_count',
        )


class BlogCommentSerializer(serializers.ModelSerializer):
    responses = SimpleBlogCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogComment
        fields = (
            'id',
            'content',
            'created_time',
            'like_count',
            'blog',
            'user',
            'serial_num',
            'is_active',
            'response_to',
            'response_serial_num',
            'response_count',
            'responses',
        )

    def create(self, validated_data):
        blog = validated_data['blog']
        blog.comment_count += 1
        serial_num = blog.comment_count
        blog.save()

        if 'response_to' in validated_data and validated_data['response_to']:
            response_to = validated_data['response_to']
            response_to.response_count += 1
            validated_data['response_serial_num'] = response_to.response_count
            response_to.save()

        comment = BlogComment.objects.create(**validated_data)
        comment.serial_num = serial_num
        comment.save()
        return comment


class TaggingBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggingBlog
        fields = (
            'id',
            'blog',
            'tag'
        )

    def create(self, validated_data):
        tagging_blog = TaggingBlog.objects.create(**validated_data)
        tagging_blog.save()
        return tagging_blog


class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = (
            'id',
            'user',
            'tag'
        )

    def create(self, validated_data):
        user_tag = UserTag.objects.create(**validated_data)
        user_tag.save()
        return user_tag


class SimpleBlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = (
            'id',
            'name',
        )


class BlogArticleSerializer(serializers.ModelSerializer):
    # tagging_blog = TaggingBlogSerializer(many=True, read_only=True)
    tags = SimpleBlogTagSerializer(many=True, read_only=True)
    comments = BlogCommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogArticle
        fields = (
            'id',
            'title',
            'description',
            'content',
            'click_count',
            'like_count',
            'word_count',
            'comment_count',
            'created_time',
            'is_active',
            'last_modified_time',
            'top',
            'category',
            'author',
            'tags'
            'comments'
            # 'tagging_blog'
            )

    def create(self, validated_data):
        blog = BlogArticle.objects.create(**validated_data)
        blog.word_count = self.count_word(validated_data['content'])
        category = validated_data['category']
        category.blog_count += 1
        category.save()
        blog.save()
        return blog

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data['title']
        if 'description' in validated_data:
            instance.description = validated_data['description']
        if 'content' in validated_data:
            instance.content = validated_data['content']
            instance.word_count = self.count_word(validated_data['content'])
        if 'top' in validated_data:
            instance.top = validated_data['top']
        if 'category' in validated_data:
            if instance.category != validated_data['category']:
                old_category = instance.category
                old_category.blog_count -= 1
                old_category.save()
                new_category = validated_data['category']
                new_category.blog_count += 1
                new_category.save()
            instance.category = validated_data['category']

        instance.last_modified_time = timezone.now()
        instance.save()
        return instance

    def count_word(self, s):
        zh_regex = re.compile(r'[\u4e00-\u9fa5|，。！？…（）：；]+')
        zh_count = 0
        en_count = 0
        en_list = []
        for w in s:
            if zh_regex.match(w):
                zh_count += 1
                en_list.append(' ')
            else:
                en_list.append(w)
        blank_regex = re.compile(r'\s+')
        words = blank_regex.split(''.join(en_list))
        for w in words:
            if w:
                en_count += 1

        return en_count + zh_count


class SimpleBlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = (
            'id',
            'name',
            'blog_count',
            'is_deletable',
            'user',
        )


class BlogCategorySerializer(serializers.ModelSerializer):
    blogs = BlogArticleSerializer(many=True, read_only=True)

    class Meta:
        model = BlogCategory
        fields = (
            'id',
            'name',
            'blog_count',
            'is_deletable',
            'user',
            'blogs',
        )

    def create(self, validated_data):
        category = BlogCategory.objects.create(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.username = validated_data['name']
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    categories = SimpleBlogCategorySerializer(many=True, read_only=True)
    blogs = BlogArticleSerializer(many=True, read_only=True)
    tags = SimpleBlogTagSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'password',
            'nick_name',
            'phone',
            'is_staff',
            'is_active',
            'gender',
            'description',
            'avatar',
            'categories',
            'blogs',
            'tags',
        )

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'nick_name' in validated_data:
            instance.nick_name = validated_data['nick_name']
        if 'phone' in validated_data:
            instance.phone = validated_data['phone']
        if 'is_staff' in validated_data:
            instance.is_staff = validated_data['is_staff']
        if 'gender' in validated_data:
            instance.gender = validated_data['gender']
        if 'description' in validated_data:
            instance.description = validated_data['description']
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        instance.save()
        return instance


class BlogTagSerializer(serializers.ModelSerializer):
    blogs = BlogArticleSerializer(many=True, read_only=True)
    users = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = BlogTag
        fields = (
            'id',
            'name',
            'blogs',
            'users',
        )

    def create(self, validated_data):
        tag = BlogTag.objects.create(**validated_data)
        tag.save()
        return tag


class LikeBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeBlog
        fields = (
            'id',
            'user',
            'blog'
        )

    def create(self, validated_data):
        blog = validated_data['blog']
        blog.like_count += 1
        blog.save()
        like_blog = LikeBlog.objects.create(**validated_data)
        like_blog.save()
        return like_blog


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = (
            'id',
            'user',
            'comment'
        )

    def create(self, validated_data):
        comment = validated_data['comment']
        comment.like_count += 1
        comment.save()
        like_comment = LikeComment.objects.create(**validated_data)
        like_comment.save()
        return like_comment


class ClickBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickBlog
        fields = (
            'id',
            'user',
            'blog')

    def create(self, validated_data):
        click_blog = ClickBlog.objects.create(**validated_data)
        click_blog.save()
        return click_blog




