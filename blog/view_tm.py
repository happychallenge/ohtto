from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from decorators import ajax_required
from django.template.loader import render_to_string

from account.models import Profile
from .models import Theme, Invitee, Post, Tag
from .forms import ThemeForm, PostForm

@login_required
def post_edit(request, id):
    post = Post.objects.prefetch_related('tag_set', 'contents').get(id=id) 
                
    if request.method == 'POST':
        form = PostForm(request.user, request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            tags = request.POST.get('tags')
            tag_array = []
            if tags:
                tag_list = tags.split(',')
                for tag in tag_list:
                    tag = tag.strip()
                    tagged, created = Tag.objects.get_or_create(tag=tag)
                    tag_array.append(tagged)
            post.tag_set.set(tag_array)

            return redirect('home')
    else:
        form = PostForm(user=request.user, instance=post)
        context = {'form': form, 'post': post}
        return render(request, 'blog/post_add.html', context)

@ajax_required
def theme_add(request):
    data = dict()
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.save(commit=False)
            theme.author = request.user
            theme.save()

            Invitee.objects.create(user=request.user, theme=theme)
            
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