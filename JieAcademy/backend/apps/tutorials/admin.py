from django.contrib import admin
from .models import UserContribution

@admin.register(UserContribution)
class UserContributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'target_id', 'target_type', 'category', 'short_content', 'likes_count', 'created_at')
    list_filter = ('target_type', 'category', 'created_at')
    search_fields = ('user__username', 'target_id', 'content')
    list_per_page = 20
    
    def short_content(self, obj):
        content = obj.content
        if len(content) > 50:
            return f"{content[:50]}..."
        return content
    short_content.short_description = '心得内容摘要'
