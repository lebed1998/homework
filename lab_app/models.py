from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
    class Meta:
        db_table = 'film'

    # Название товара
    name = models.CharField(max_length=255)

    # Описание товара
    description = models.CharField(max_length=1000)

    # Режиссёр
    director = models.CharField(max_length=255)

    # Ссылка на картинку фильма
    image = models.ImageField(upload_to='lab_app/static/film_images',
                              default='lab_app/static/film_images/default.png')

    # Полный путь до картинки фильма
    def image_path(self):
        return self.image.name.replace('lab_app/', '/')

    # Короткое описание фильма
    def short_description(self):
        return self.description[:126]

    def __str__(self):
        return ' '.join([
            self.name,
            ' from ',
            self.director,
        ])


class User(models.Model):
    class Meta:
        db_table = 'user'

    # почта
    email = models.CharField(max_length=255)

    # имя
    first_name = models.CharField(max_length=255)

    # фамилия
    last_name = models.CharField(max_length=255)

    # пароль
    password = models.CharField(max_length=128)

    # ник
    username = models.CharField(max_length=255)


class Review(models.Model):
    class Meta:
        db_table = 'review'

    # Пользователь, который оставил отзыв
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Фильм, на который оставлен отзыв
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    # Текст отзыва
    description = models.CharField(
        max_length=500,
    )

    def __str__(self):
        return ' '.join([
            'review \'',
            str(self.description),
            ' \' from user @',
            str(self.user.username),
        ])
