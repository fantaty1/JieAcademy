from django.db import models
from django.conf import settings


class UserContribution(models.Model):
    CATEGORY_CHOICES = [
        ('combo', '连招分享'),
        ('insight', '实战感悟'),
    ]

    TARGET_TYPE_CHOICES = [
        ('weapon', '武器'),
        ('hero', '英雄'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions', verbose_name='作者'
    )
    target_id = models.CharField('目标ID', max_length=50, help_text="如 'changjian', 'jianan' 等硬编码ID")
    target_type = models.CharField('目标类型', max_length=20, choices=TARGET_TYPE_CHOICES)
    category = models.CharField('内容分类', max_length=20, choices=CATEGORY_CHOICES, default='insight')
    content = models.TextField('心得内容(Markdown)', blank=False)
    
    # Optional fields for future expansion
    likes_count = models.IntegerField('点赞数', default=0)

    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_contributions'
        verbose_name = '玩家心得'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.target_id} ({self.get_category_display()})"
