from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Notification

@login_required
def notifications(request):
    notifications = Notification.objects.filter(to_user=request.user)
    unread = Notification.objects.filter(to_user=request.user, is_read=False)

    for notification in unread:
        notification.is_read = True
        notification.save()

    return render(request, 'activity/notifications.html', {
            'notifications': notifications,
        })

@login_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)[:8]

    for notification in notifications:
        notification.is_read = True 
        notification.save()

    return render(request, 'activity/partial/last_notifications.html', {
            'notifications': notifications,
        })

@login_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False).count()
    return HttpResponse(notifications)