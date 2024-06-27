from django.urls import path
from . import views

app_name = 'crud'
urlpatterns = [
    path('detail/<int:post_id>/<slug:post_slug>/', views.DetailView.as_view(), name='detail'),
    path('posts', views.PostsView.as_view(), name='posts')
]