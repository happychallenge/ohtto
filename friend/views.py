import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Profile
from .models import FriendshipRequest
from account.models import Relation
# Create your views here.
@login_required
def friend_list(request, tag=None):

  # Friend List
    friend_list = request.user.profile.get_following
  # Already asking Friendship List
    qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
        from_user=request.user.profile).all()
    asking_friends = [u.to_user for u in qs]

    querylist = Profile.objects.exclude(
        follower_user__from_user=request.user.profile)
    recommend_list = querylist.exclude(follower_user__to_user__in=asking_friends)

  # Have received asking Friendship List
    qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
            to_user=request.user.profile, rejected=False).all()
    received_list = [u.from_user for u in qs]

    qs = FriendshipRequest.objects.filter(to_user=request.user.profile, rejected=True) 
    rejected_list = [u.from_user for u in qs]

    context = {'friend_list': friend_list, 'recommend_list': recommend_list, 
                'received_list': received_list, 'rejected_list': rejected_list}
    return render(request, 'friend/friend.html', context)


@login_required
def ask_friend(request):
    from_user = request.user.profile
    id = request.POST.get('pk')
    if id:
        to_user = Profile.objects.get(id=id)

    if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")
    if to_user in from_user.get_following:
        message = "Users are already friends"

    request, created = FriendshipRequest.objects.get_or_create(
        from_user=from_user,
        to_user=to_user,
    )

    if created is False:
        message = "You already requested friendship to {}".format(to_user)
    else:
        message = "You have requested friendship to {} successfully".format(to_user)
    context = { 'message' : message }
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def accept_friend(request):
    from_user = request.user.profile
    id = request.POST.get('pk')
    if id:
        to_user = Profile.objects.get(id=id)

    relation1 = Relation.objects.create(
        from_user=from_user,
        to_user=to_user,
        status='F'
    )
    relation2 = Relation.objects.create(
        from_user=to_user,
        to_user=from_user,
        status='F'
    )

    FriendshipRequest.objects.get(from_user=to_user, to_user=from_user).delete()

    friend_list = request.user.profile.get_following
    return render(request, "friend/ajax_friend_list.html", { 'friend_list': friend_list})

@login_required
def reject_friend(request):
    to_user = request.user.profile
    id = request.POST.get('pk')
    if id:
        from_user = Profile.objects.get(id=id)

    fsr = FriendshipRequest.objects.get(from_user=from_user, to_user=to_user)
    fsr.rejected = True
    fsr.save()

    qs = FriendshipRequest.objects.filter(to_user=to_user, rejected=True) 
    rejected_list = [u.from_user for u in qs]
    return render(request, "friend/ajax_rejected_list.html", { 'rejected_list': rejected_list})

