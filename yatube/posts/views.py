from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .constants import POSTS_GROUP_POSTS_PAGE_LIM, POSTS_INDEX_PAGE_LIM
from .forms import PostForm
from .utils import paginator


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.select_related(
        'group')

    page_obj = paginator(posts, POSTS_INDEX_PAGE_LIM, request)

    context = {
        'page_obj': page_obj,
    }

    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.select_related(
        'group').filter(group=group)

    page_obj = paginator(posts, POSTS_GROUP_POSTS_PAGE_LIM, request)

    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.select_related(
        'author').filter(author=user)

    page_obj = paginator(posts, POSTS_INDEX_PAGE_LIM, request)

    context = {
        'author': user,
        'page_obj': page_obj,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_det = get_object_or_404(Post, pk=post_id)

    posts = Post.objects.select_related(
        'author').filter(author=post_det.author)
    posts_cnt = len(posts)

    context = {
        'post_det': post_det,
        'posts_cnt': posts_cnt,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    is_edit = False
    form = PostForm(request.POST or None)

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        author = request.user.username

        new_post.save()

        return redirect(f'/profile/{author}/')

    context = {
        'form': form,
        'is_edit': is_edit,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post_det = Post.objects.select_related(
        'group').get(pk=post_id)

    if post_det.author == request.user:
        form = PostForm(request.POST or None, instance=post_det)

        if form.is_valid() and request.method == 'POST':
            form.author = request.user
            form.save()

            return redirect(f'/posts/{post_id}/')

        is_edit = True
        context = {
            'form': form,
            'is_edit': is_edit,
        }

        return render(request, 'posts/create_post.html', context)

    else:

        return redirect(f'/posts/{post_id}/')
