import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from PIL import Image
from dateutil import parser
from clarifai.rest import ClarifaiApp

from .models import Post, Tag, Content, Theme, Bucket
from .forms import PostForm
from .getGPS import get_lat_lon_dt
from .adjust_location import transform

app = ClarifaiApp(api_key='b207516379df44bfbcd5ba1c32514b41')
model = app.models.get('general-v1.3')
forbidden = ['backlit', 'light', 'no person', 'silhouette', 'sky']

# Create your views here.
@login_required
def index(request, tag=None):
    friend_set = request.user.profile.get_following

    if tag:
        post_list = Post.objects.filter(is_published=True, author__profile__in=friend_set,
                            tag_set__tag__iexact=tag) \
            .prefetch_related('tag_set', 'like_user_set__profile', 'contents', 'comments', 'bucket_set') \
            .select_related('author__profile')[:50]
        context = {'post_list': post_list, 'tag': tag}
    else:
        post_list = Post.objects.filter(is_published=True, author__profile__in=friend_set) \
            .prefetch_related('tag_set', 'like_user_set__profile', 'contents', 'comments', 'bucket_set') \
            .select_related('author__profile')[:50]
        context = {'post_list': post_list,}
    return render(request, 'blog/index.html', context)


def post_detail(request):
    id = request.GET.get('id')
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/partial/post_detail.html', {'post': post})


@login_required
def my_history(request):
    post_list = Post.objects.filter(author=request.user)
    return render(request, 'blog/on_map.html', {'post_list':post_list})


def user_theme_list(request, username, id):
    theme = get_object_or_404(Theme, id=id)
    if request.user.username == username:
        post_list = Post.objects.filter(theme=theme)
        context = {'post_list':post_list}
    else:
        if theme.status == True:
            post_list = Post.objects.filter(theme=theme)
            context = {'post_list':post_list}
        else:
            context = {'message': "You don't have a privilage to access these content"}
    return render(request, 'blog/on_map.html', context)


@login_required
def current_location(request,tag=None):
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))

    if tag:
        post_list = Post.objects.filter(is_published=True, 
            lat__range=(lat - 0.3, lat + 0.3), lng__range=(lng - 0.3, lng + 0.3),
            tag_set__tag__iexact=tag) \
                .prefetch_related('tag_set', 'like_user_set__profile', 'contents', 'comments', 'bucket_set') \
                .select_related('author__profile')[:50]
        context = {'post_list': post_list, 'tag': tag, 'pos': True}
    else:
        post_list = Post.objects.filter(is_published=True, 
            lat__range=(lat - 0.3, lat + 0.3), lng__range=(lng - 0.3, lng + 0.3)) \
                .prefetch_related('tag_set', 'like_user_set__profile', 'contents', 'comments', 'bucket_set') \
                .select_related('author__profile')[:50]
        context = {'post_list': post_list, 'pos': True}
    return render(request, 'blog/index.html', context)


@login_required
def my_bucket_list(request):
    post_list = request.user.profile.get_bucket_list
    return render(request, 'blog/on_map.html', {'post_list':post_list})


@login_required
@require_POST
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_like, created = post.like_set.get_or_create(user=request.user)

    if not created:
        post_like.delete()
        message = "Cancel like"
    else:
        message = "Like"
        request.user.profile.notify_post_liked(post)
    context = {
        'like_count': post.like_count, 'message': message,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
@require_POST
def post_bucket(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_like, created = post.bucket_set.get_or_create(user=request.user)

    if not created:
        post_like.delete()
        message = "Cancel the bucket List"
    else:
        message = "Add the post into bucket List"
        request.user.profile.notify_post_bucketed(post)

    context = {
        'bucket_count': post.bucket_count, 'message': message,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            pictures = request.FILES.getlist('pictures')
            tag_total = set()
        # Multi Files
            for filename in pictures:
                content = Content()
            # Read Position from Picture
                image = Image.open(filename)
                lat, lng, dt = get_lat_lon_dt(image)
                mgLat, mgLng = transform(lat, lng)
                if mgLat:
                    content.lat = mgLat
                    content.lng = mgLng
                if dt:
                    dt = parser.parse(dt)
                    content.taken_dt = dt

                width, height = image.size
                x = width * 0.5
                y = height * 0.5
                image.thumbnail((x, y), Image.ANTIALIAS)
                image.save(filename, quality=90)
                
                content.file = filename
                content.save()
                post.contents.add(content)

                response = model.predict_by_filename('.' + content.file.url)
                concepts = response['outputs'][0]['data']['concepts']
                tag_array = []
                for concept in concepts:
                    if concept['value'] > 0.95:
                        if concept['name'] not in forbidden:
                            obj, created = Tag.objects.get_or_create(tag=concept['name'])
                            tag_array.append(obj)
                content.tag_set.set(tag_array)
                tag_total.update(tag_array)

            tag_total = list(tag_total)
            post.tag_set.set(tag_total)
            post.lat = mgLat
            post.lng = mgLng
            post.save()
            
            return redirect('blog:index')

    else:
        form = PostForm(user=request.user)
        return render(request, 'blog/post_add.html', {'form': form})




