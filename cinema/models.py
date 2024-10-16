from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Моделька категорий
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')

    def __str__(self):
        return self.title

    # Умная ссылка для категорий
    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# blank=True, null=True  - данной командой говорим что поле не обязательно для заполнения
class Cinema(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название фильма')
    content = models.TextField(verbose_name='Описание фильма')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    video = models.CharField(max_length=250, blank=True, null=True, verbose_name='Ссылка видео')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория фильма')
    author = models.ForeignKey(User, on_delete=models.CASCADE,  verbose_name='Автор', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cinema_detail', kwargs={'pk': self.pk})

    # Метод для получения картинки кинфильма
    def get_photo_cinema(self):
        try:
            return self.photo.url
        except:
            return 'https://images.satu.kz/184881622_w500_h500_yaschik-dlya-instrumenta.jpg'

    class Meta:
        verbose_name = 'Кинофильм'
        verbose_name_plural = 'Кинофильмы'




# Модель комментария
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Коментатор')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Кинофильм')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Комментрий'
        verbose_name_plural = 'Комментрии'



# Моделька профиля
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Фото')
    phone_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер')
    about_me = models.CharField(max_length=200, blank=True, null=True, verbose_name='О себе')
    publisher = models.BooleanField(default=True, verbose_name='Право добавления видео')

    def __str__(self):
        return self.user.username

    # Метод для получения фото профиля
    def get_photo(self):
        try:
            return self.photo.url
        except:
            return 'https://list.yablogo.su/wp-content/uploads/2020/07/orio.png'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'



