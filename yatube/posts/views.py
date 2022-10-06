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
        'author').filter(group=group)

    page_obj = paginator(posts, POSTS_GROUP_POSTS_PAGE_LIM, request)

    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.select_related(
        'group').filter(author=user)

    page_obj = paginator(posts, POSTS_INDEX_PAGE_LIM, request)

    context = {
        'author': user,
        'page_obj': page_obj,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_det = get_object_or_404(Post, pk=post_id)

    context = {
        'post_det': post_det,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    is_edit = 'create'
    form = PostForm(request.POST or None)

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()

        return redirect('posts:profile', username=request.user.username)

    context = {
        'form': form,
        'is_edit': is_edit,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post_det = Post.objects.select_related(
        'group').get(pk=post_id)

    form = PostForm(request.POST or None, instance=post_det)

    if post_det.author != request.user:

        return redirect('posts:post_detail', post_id=post_id)

    elif form.is_valid():
        form.author = request.user
        form.save()

        return redirect('posts:post_detail', post_id=post_id)

    else:
        is_edit = 'edit'
        context = {
            'form': form,
            'is_edit': is_edit,
        }

        return render(request, 'posts/create_post.html', context)
