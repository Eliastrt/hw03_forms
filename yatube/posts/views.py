from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User
from .constants import POSTS_INDEX_LIM, POSTS_GROUP_POSTS_LIM, \
    POSTS_GROUP_POSTS_PAGE_LIM, POSTS_INDEX_PAGE_LIM
from .forms import PostForm


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.select_related(
        'group')[:POSTS_INDEX_LIM]

    paginator = Paginator(posts, POSTS_INDEX_PAGE_LIM)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.select_related(
        'group').filter(group=group)[:POSTS_GROUP_POSTS_LIM]

    paginator = Paginator(posts, POSTS_GROUP_POSTS_PAGE_LIM)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.select_related(
        'author').filter(author=user)

    author = user

    posts_cnt = len(posts)
    paginator = Paginator(posts, POSTS_INDEX_PAGE_LIM)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'posts_cnt': posts_cnt,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post_det = Post.objects.select_related(
        'group').get(pk=post_id)

    post_short = post_det.text[0:30]

    posts = Post.objects.select_related(
        'author').filter(author=post_det.author)
    posts_cnt = len(posts)

    context = {
        'post_det': post_det,
        'posts_cnt': posts_cnt,
        'post_short': post_short,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    username = request.user.username
    user = request.user
    is_edit = False

    if request.user.is_authenticated and request.method == 'POST':

        form = PostForm(request.POST)

        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            new_post = form.save(commit=False)
            new_post.author = user
            author = username

            new_post.save()

            return redirect('/profile/%s/' % author)

        # Если условие if form.is_valid() ложно и данные не прошли валидацию -
        # передадим полученный объект в шаблон,
        # чтобы показать пользователю информацию об ошибке

        # Заодно заполним все поля формы данными, прошедшими валидацию,
        # чтобы не заставлять пользователя вносить их повторно
        context = {
            'form': form,
            'is_edit': is_edit,
        }
        return render(request, 'posts/create_post.html', context)

        # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
        # пусть пользователь напишет что-нибудь
    form = PostForm()
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    post_det = Post.objects.select_related(
        'group').get(pk=post_id)

    user = request.user

    if request.user.is_authenticated and post_det.author == user:

        if request.method == 'POST':

            form = PostForm(request.POST, instance=post_det)

            if form.is_valid():
                form.author = user
                form.save()
                return redirect('/posts/%s/' % post_id)

            is_edit = True
            context = {
                'form': form,
                'is_edit': is_edit,
            }
            return render(request, 'posts/create_post.html', context)

        form = PostForm(instance=post_det)

        is_edit = True
        context = {
            'form': form,
            'is_edit': is_edit,
        }
        return render(request, 'posts/create_post.html', context)

    else:
        return redirect('/posts/%s/' % post_id)
