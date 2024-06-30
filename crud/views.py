from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CreateUpdateForm, CommentForm, ReplyForm, SearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostsView(View):
    form_class = SearchForm
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(title__contains=request.GET['search'])
        return render(request, 'crud/posts.html', {'posts': posts, 'form': self.form_class})


class DetailView(View):
    form_class = CommentForm
    form_class_reply = ReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):
        comments = self.post_instance.post_comments.filter(is_reply=False)
        can_vote = True
        if request.user.is_authenticated and self.post_instance.is_vote(request.user):
            can_vote = False
        return render(request, 'crud/detail.html', {'post': self.post_instance, 'comments': comments, 'form': self.form_class, 'reply': self.form_class_reply, 'can_vote': can_vote})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your comment has been submitted.', 'success')
            return redirect('crud:detail',  self.post_instance.id, self.post_instance.slug)


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


class ReplyView(LoginRequiredMixin, View):
    form_class = ReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'you reply submitted successfully', 'success')
        return redirect('crud:detail', post.id, post.slug)


class VoteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this post', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'you liked this post', 'success')
        return redirect('crud:detail', post.id, post.slug)