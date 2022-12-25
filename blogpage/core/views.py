import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from blog.forms import CommentForm
from blog.models import Post, Category
from django.http import JsonResponse


@csrf_exempt
def create_post(request):
    if request.method == 'GET':
        return render(request, 'core/create_post.html')
    else:
        cat = Category.objects.all()
        created_post = Post.objects.create(
            title=request.POST['title'],
            body=request.POST['body'],
            slug=slugify(request.POST['title']),
            intro='default intro',
            status=Post.ACTIVE,
            category=cat[0])
        return redirect(f'/post/{created_post.id}/')


def frontpage(request):
    posts = Post.objects.all()
    post_list = []
    for post in posts:
        post_preview = {
            "title": post.title,
            "intro": post.intro,
            "created_at": post.created_at,
            "body": post.body[:20],
            "id": post.id,
            "status": post.status
        }
        post_list.append(post_preview)
    return render(request, 'core/frontpage.html', {"posts": post_list})


def about(request):
    return render(request, 'core/about.html')


def single_post(request, id):
    id = int(id)
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('single_post', id=id)
        else:
            form = CommentForm()

    forms = CommentForm()
    return render(request, 'core/post_display.html', {"post": post, "form": forms})


def new_blog(request):
    return render(request, 'core/new_blog.html')


def category(request, id):
    if not request.user.has_perm("blog.view_category"):
        return render(request, 'core/permission.html')

    # category = Category.objects.all()
    category = get_object_or_404(Category, id=id)

    return render(request, 'core/category.html', {'category': category})


@csrf_exempt
def rest_post(request, id=None):
    if request.method == 'GET':
        id = int(id)
        post = Post.objects.get(id=id)
        return JsonResponse(post.to_dict())

    elif request.method == 'POST':
        cat = Category.objects.all()
        dbdict = json.load(request)
        created_post = Post.objects.create(
            title=dbdict.get('title'),
            body=dbdict.get('body'),
            slug=slugify(dbdict.get('title')),
            intro=dbdict.get('intro'),
            status=Post.ACTIVE,
            category=cat[0])
        post = Post.objects.get(id=created_post.id)
        return JsonResponse(post.to_dict())

    elif request.method == 'PUT':
        return JsonResponse({'foo': 'put'})

    elif request.method == 'DELETE':
        return JsonResponse({'foo': 'delete'})


@csrf_exempt
def rest_posts(request):
    pass