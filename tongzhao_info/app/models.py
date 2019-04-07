# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib import admin

# Create your models here.

# class Project(models.Model):
#     project_name = models.CharField(max_length=200)
#     project_url = models.URLField()
#     project_author = models.CharField(max_length=200)
#     project_description = models.TextField()
#     project_image = models.ImageField()


class Image(models.Model):
    image = models.ImageField(upload_to='img')
    image_name = models.CharField(max_length=200, null=True)


class CustomUser(AbstractUser):
    phone_validator = UnicodeUsernameValidator()
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=60,
        unique=True,
        help_text=_('Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email_validator = UnicodeUsernameValidator()

    email = models.EmailField(_('email address'),
                              max_length=60,
                              validators=[email_validator],
                              unique=True,
                              help_text=_('Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                              error_messages = {
                         'unique': _("A user with the same email already exists."),
                     },)

    phone = models.CharField(
                            _('phone'),
                            max_length=15,
                            unique=True,
                            null=True, blank=True,
                            validators = [phone_validator],
                            error_messages = {
                                'unique': _("A user with the phone number already exists."),
                            },
    )

    nick_name = models.CharField(_('nick name'), max_length=50, default='')
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.CharField(_('gender'), max_length=6, choices=(('m', 'male'), ('f', 'female')), default='female', )
    description = models.CharField(_('description'), max_length=280, null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatar/', null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    tags = models.ManyToManyField('BlogTag', through='UserTag', verbose_name=_('tags'))

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'gender']

    class Meta:
        verbose_name = _('custom user')
        verbose_name_plural = _('custom users')
        app_label = 'app'

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username


class BlogCategory(models.Model):
    name = models.CharField(_('category name'), max_length=60)
    created_time = models.DateTimeField(_('created time'), default=timezone.now)
    blog_count = models.IntegerField(_('blog count'), default=0)
    user = models.ForeignKey(CustomUser, related_name='categories', to_field='username', on_delete=models.CASCADE)
    is_deletable = models.BooleanField(_('is deletable'), default=True)

    class Meta:
        unique_together = ('name', 'user',)
        ordering = ['-created_time']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class BlogTag(models.Model):
    name = models.CharField(verbose_name=_('tag name'), unique=True, max_length=66)
    created_time = models.DateTimeField(verbose_name=_('created time'), default=timezone.now)
    blogs = models.ManyToManyField('BlogArticle', through='TaggingBlog', verbose_name='blogs')
    users = models.ManyToManyField('CustomUser', through='UserTag', verbose_name='users')

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class BlogArticle(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    content = models.TextField(_('content'), blank=True)
    click_count = models.IntegerField(_('click_count'), default=0)
    like_count = models.IntegerField(_('like_count'), default=0)
    word_count = models.IntegerField(_('word count'), default=0)
    comment_count = models.IntegerField(_('comment_count'), default=0)
    created_time = models.DateTimeField(_('created time'), default=timezone.now)
    last_modified_time = models.DateTimeField('last modified time', default=timezone.now)
    top = models.BooleanField('top', default=False)
    is_private = models.BooleanField(_('is private'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    category = models.ForeignKey(BlogCategory, related_name='blogs', null=True, verbose_name=_('category'), on_delete=models.SET_NULL)
    author = models.ForeignKey(CustomUser, related_name='blogs', to_field='username', verbose_name=_('author'), on_delete=models.CASCADE)
    tags = models.ManyToManyField(BlogTag, through='TaggingBlog', verbose_name='tags')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-top', '-last_modified_time']


class TaggingBlog(models.Model):
    tag = models.ForeignKey(BlogTag, related_name='tagging_blog', verbose_name=_('tag'), on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogArticle, related_name='tagging_blog', verbose_name=_('blog'), on_delete=models.CASCADE)
    created_time = models.DateTimeField(verbose_name=_('created time'), default=timezone.now)

    class Meta:
        ordering = ['-created_time']
        unique_together = ('tag', 'blog',)


class UserTag(models.Model):
    tag = models.ForeignKey(BlogTag, related_name='user_tag', verbose_name=_('tag'), on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user_tag', verbose_name=_('user'), on_delete=models.CASCADE)
    created_time = models.DateTimeField(verbose_name=_('created time'), default=timezone.now)

    class Meta:
        ordering = ['-created_time']
        unique_together = ('tag', 'user',)

class BlogComment(models.Model):
    content = models.TextField()
    serial_num = models.IntegerField(_('serial num'), default=1)
    created_time = models.DateTimeField(_('created time'), default=timezone.now)
    like_count = models.IntegerField(_('like count'), default=0)
    is_active = models.BooleanField(_('active'), default=True)
    is_hot = models.BooleanField(_('hot'), default=False)
    blog = models.ForeignKey(BlogArticle, related_name='comments', verbose_name=_('blog'), on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='comments', to_field='username' , verbose_name=_('user'), on_delete=models.CASCADE)
    response_to = models.ForeignKey('self', related_name='responses', null=True, verbose_name=_('reply to'), on_delete=models.SET_NULL)
    response_serial_num = models.IntegerField(_('response serial num'), default=0)
    response_count = models.IntegerField(_('response count'), default=0)

    class Meta:
        # ordering = ['-is_hot', 'like_count', '-created_time']
        ordering = ['-created_time']


class LikeBlog(models.Model):
    created_time = models.DateTimeField(_('created time'), default=timezone.now)
    user = models.ForeignKey(CustomUser, related_name='like_blog', to_field='username', verbose_name=_('user'), on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogArticle, related_name='like_blog', verbose_name=_('blog'), on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_time']
        unique_together = ('user', 'blog')


class LikeComment(models.Model):
    created_time = models.DateTimeField(_('created time'), default=timezone.now)
    user = models.ForeignKey(CustomUser, related_name='like_comment', to_field='username', verbose_name=_('user'), null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(BlogComment, related_name='like_comment', verbose_name=_('comment'), on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_time']
        unique_together = ('user', 'comment')


class ClickBlog(models.Model):
    created_time = models.DateTimeField(_('created time'), default=timezone.now)
    user = models.ForeignKey(CustomUser, related_name='click_blog', to_field='username', verbose_name=_('user'), on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogArticle, related_name='click_blog', verbose_name=_('blog'), on_delete=models.CASCADE)






