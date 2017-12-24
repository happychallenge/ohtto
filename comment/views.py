from django.shortcuts import render, get_object_or_404
from .models import Comment
from blog.models import Post
from .forms import CommentForm

# Create your views here.
def post_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        post_id = request.POST.get('post')
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_user = user
            comment.save()
            user.profile.notify_post_commented(post)

        comment_list = Comment.objects.filter(post = post)
        return render(request, 'comment/comment.html',
            { 'comment_list': comment_list, 'post_id': post_id })

    else:
        post_id = request.GET.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        comment_list = Comment.objects.filter(post = post)
        return render(request, 'comment/comment.html',
            { 'comment_list': comment_list, 'post_id': post_id})