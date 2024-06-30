from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/done', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnfollowView.as_view(), name='unfollow'),
    path('profile/edit-profile/', views.EditProfileView.as_view(), name='edit_profile')
]