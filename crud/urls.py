from django.urls import path
from . import views

app_name = 'crud'
urlpatterns = [
    path('posts/detail/<int:post_id>/<slug:post_slug>/', views.DetailView.as_view(), name='detail'),
    path('posts', views.PostsView.as_view(), name='posts'),
    path('posts/delete/<int:post_id>/', views.DeleteView.as_view(), name='delete'),
    path('posts/update/<int:post_id>/', views.UpdateView.as_view(), name='update'),
    path('posts/create/', views.CreateView.as_view(), name='create'),
    path('posts/reply/<int:post_id>/<int:comment_id>/', views.ReplyView.as_view(), name='reply'),
    path('post/like/<int:post_id>/', views.VoteView.as_view(), name='vote')
]