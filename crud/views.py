from django.shortcuts import render
from django.views import View
from .models import Post


class PostsView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'crud/posts.html', {'posts': posts})


class DetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(id=post_id, slug=post_slug)
        return render(request, 'crud/detail.html', {'post': post})