from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Profile
# Create your views here.
@login_required
def friend_list(request, tag=None):
    friend_list = request.user.profile.get_following


    recommend_list = Profile.objects.exclude(
        follower_user__from_user=request.user.profile)[:5]

    context = {'friend_list': friend_list, 'recommend_list': recommend_list}
    return render(request, 'friend/friend_list.html', context)
