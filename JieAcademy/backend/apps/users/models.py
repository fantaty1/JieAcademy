from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    avatar = models.CharField('头像', max_length=255, blank=True, default='')
    is_admin = models.BooleanField('是否管理员', default=False)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
