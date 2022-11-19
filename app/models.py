from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.title}'

    class Meta: 
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    title = models.CharField('название', max_length=25)
    image = models.ImageField(upload_to='post/%Y/%m/%d/')
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE ,verbose_name = 'автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категории')
    slug = models.SlugField(max_length=255) 
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.title}'

    class Meta: 
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class CommentPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.user} -> {self.post}'

    class Meta: 
        verbose_name = 'Комментарий к посту'
        verbose_name_plural = 'Комментарии к постам'


class CommentCity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.user} -> {self.city}'

    class Meta: 
        verbose_name = 'Комментарий к городу'
        verbose_name_plural = 'Комментарии к городам'

class Star(models.Model):

    star = models.IntegerField()

    def __str__(self):
        return f'{self.star}'

    class Meta:
        verbose_name = 'Звезда'
        verbose_name_plural = 'Звезды'

class Rating(models.Model):

    star = models.ForeignKey(Star, on_delete=models.CASCADE, verbose_name='рейтинг')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост')

    def __str__(self):
        return f'{self.user}->{self.post} star:{self.star}'

    class Meta: 
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class City(models.Model):

    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='city/%Y/%m/%d/')
    min_description = models.TextField(max_length=1000)
    text = models.TextField()

    def save(self, *args, **kwargs):
            self.title_ru = self.title_ru.title()
            self.title_eng = self.title_eng.title()
            return super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title_ru}'

    class Meta: 
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Follow(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, verbose_name='пользователь', related_name='user')
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='подписчик', related_name='follower')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} -> {self.user} date:{self.date}'

    class Meta: 
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class Task(models.Model):
    title = models.CharField(max_length=250, verbose_name='название')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    description = models.TextField(max_length=2000, verbose_name='описание', blank=True, null=True)

    def __str__(self):
        return f'title: {self.title}  user: {self.user}'

    class Meta: 
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

