from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.core.paginator import Paginator

from .forms import PostForm, CommentForm
from .models import Post, Group, Follow

User = get_user_model()
# Create your views here.
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)

def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Лев Толстой – зеркало русской революции.'
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)

def profile(request, username):

    following_user = get_object_or_404(User, username=username)

    following = Follow.objects.filter(author=following_user, user=request.user)
    print(following)
    posts = Post.objects.filter(author__username=username).order_by('-pub_date')
    count_posts = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Профайл пользователя {username}'

    context = {
        'page_obj': page_obj,
        'count_posts': count_posts,
        'title': title,
        'username': username,
        'following': following,
    }

    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    print(comments)
    comment_form = CommentForm()
    if post.group:
        group = get_object_or_404(Group, slug=post.group.slug)
    else:
        group = None
    posts_count_by_author = Post.objects.filter(author__username=post.author).count()
    title = f'Пост {post.text[:30]}'

    context = {
        'title': title,
        'post': post,
        'group': group,
        'posts_count_by_author': posts_count_by_author,
        'comment_form': comment_form,
        'comments': comments,
    }

    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    form = PostForm()
    context = {'form': form}
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(
                'posts:profile', post.author.username
            )
    return render(request, template_name=template, context=context)

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def profile_follow(request, username):

    following = get_object_or_404(User, username=username)
    follower = request.user
    if follower != following and follower != following.follower:
        Follow.objects.get_or_create(user=follower, author=following)
    return redirect('posts:profile', username=username)

@login_required
def profile_unfollow(request, username):
    following = get_object_or_404(User, username=username)
    Follow.objects.filter(
        user=request.user,
        author=following
    ).delete()
    return redirect('posts:profile', username)


@login_required
def follow_index(request):
    user = request.user
    follow_authors = Follow.objects.filter(user=user).values_list('author_id', flat=True)
    posts = Post.objects.filter(author__in=follow_authors).order_by('-pub_date')
    print(posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)

