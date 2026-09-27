from email.mime import image
from time import timezone

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class article(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles', verbose_name='نویسنده'
    )
    category = models.ManyToManyField(
        Category, related_name='articles', verbose_name='دسته بندی'
    )  # if you dont need to Reverse relation you can replace related name to '+'
    title = models.CharField(max_length=200, blank=True, verbose_name='عنوان')
    content = models.TextField(blank=True, verbose_name='محتوا')
    created = models.DateField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated = models.DateField(auto_now=True, blank=True, verbose_name='تاریخ بروزرسانی')
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر')
    slug = models.SlugField(unique=True, blank=True, verbose_name='اسلاگ')

    def __str__(self):
        return self.title

    def show_image(self):
        if self.image:
            return format_html('<img src="{}" width="60" height="40">', self.image.url)
        return format_html('<h3 style="color:red">تصویر ندارد</h3>')

    show_image.short_description = 'تصویر'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # اگر اسلاگ خالی بود، از روی عنوان بساز
        if not self.slug:
            # پارامتر allow_unicode=True باعث میشه کاراکترهای فارسی حفظ بشن
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name='نویسنده'
    )
    article = models.ForeignKey(
        article, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله'
    )
    image = models.ImageField(
        upload_to='images/comments', null=True, blank=True, verbose_name='تصویر'
    )
    content = models.TextField(verbose_name='متن نظر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='replies', verbose_name='پاسخ به'
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class Message(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True, verbose_name='نام')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='سن')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f"{self.name}-{self.subject}"

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'




class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes',verbose_name='کاربر')
    article = models.ForeignKey(article,on_delete=models.CASCADE,related_name='likes',verbose_name='مقاله')
    Date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.article}"

    class Meta:
        verbose_name='لایک'
        verbose_name_plural = 'لایک ها'
        ordering = ['-Date']