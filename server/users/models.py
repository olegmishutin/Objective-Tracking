import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    photo = models.ImageField('фотография', upload_to='users_photos/', blank=True, null=True)
    first_name = models.CharField('имя', max_length=128)
    last_name = models.CharField('фамилия', max_length=128)
    email = models.EmailField('email', unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'User'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def changePhoto(self, file=None):
        if file:
            if self.photo and os.path.exists(self.photo.path):
                os.remove(self.photo.path)

            self.photo = file

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()
