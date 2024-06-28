from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CreateUpdateForm
from django.utils.text import slugify


class PostsView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'crud/posts.html', {'posts': posts})


class DetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, 'crud/detail.html', {'post': post})


class DeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully', 'success')
            return redirect('crud:posts')
        else:
            messages.error(request, 'You do not have permission to delete this post', 'danger')
            return redirect('crud:detail', post.id, post.slug)


class UpdateView(LoginRequiredMixin, View):
    form_class = CreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'You do not have permission to update this post', 'danger')
            return redirect('crud:posts')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'crud/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            ns = form.save(commit=False)
            ns.slug = slugify(form.cleaned_data['title'])
            ns.save()
            messages.success(request, 'Post updated successfully', 'success')
            return redirect('crud:detail', post.id, post.slug)
        else:
            messages.error(request, 'You do not have permission to update this post', 'danger')
            return redirect('crud:detail', post.id, post.slug)


class CreateView(LoginRequiredMixin, View):
    form_class = CreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'crud/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            ns = form.save(commit=False)
            ns.slug = slugify(form.cleaned_data['title'])
            ns.body = form.cleaned_data['body']
            ns.user = request.user
            ns.save()
            messages.success(request, 'Post created successfully', 'success')
            return redirect('crud:detail', ns.id, ns.slug)