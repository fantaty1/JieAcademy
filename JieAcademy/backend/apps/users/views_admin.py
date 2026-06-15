from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from apps.tutorials.models import UserContribution
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    today = timezone.now().date()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    total_contributions = UserContribution.objects.count()

    # User trend (last 7 days)
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    user_trend_labels = [d.strftime('%m-%d') for d in dates]
    user_trend_data = []
    for d in dates:
        count = User.objects.filter(date_joined__date=d).count()
        user_trend_data.append(count)

    # Content category
    category_counts = UserContribution.objects.values('category').annotate(count=Count('id'))
    category_data = []
    for item in category_counts:
        name = '连招分享' if item['category'] == 'combo' else '实战感悟'
        category_data.append({'name': name, 'value': item['count']})

    context = {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'total_contributions': total_contributions,
        'user_trend_labels': user_trend_labels,
        'user_trend_data': user_trend_data,
        'category_data': category_data,
    }
    return render(request, 'admin/custom_dashboard.html', context)
