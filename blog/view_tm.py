from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404

from decorators import ajax_required
from django.template.loader import render_to_string

from account.models import Profile
from .models import Theme, Invitee
from .forms import ThemeForm

@ajax_required
def theme_add(request):
    data = dict()
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.save(commit=False)
            theme.author = request.user
            theme.save()

            persons_id = request.POST.getlist('persons_id')

            if persons_id:
                for person_id in persons_id:
                    person = get_object_or_404(Profile, id=person_id)
                    to_user = person.user
                    obj, created = Invitee.objects.get_or_create(user=to_user, theme=theme)

                    if created:
                        request.user.profile.notify_theme_invited(theme, to_user)

            return redirect('user_profile')

        else:
            data['status'] = False;
            data['html_form'] = render_to_string('blog/theme_add.html', {'form':form}, request=request)

    else:
        form = ThemeForm()

    data['html_form'] = render_to_string('blog/theme_add.html', {'form':form}, request=request)
    return JsonResponse(data)