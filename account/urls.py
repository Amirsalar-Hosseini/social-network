from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/Done', views.UserPasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('reset/complete', views.UserPasswordResetConfirmView.as_view(), name='reset_password_complete'),
]