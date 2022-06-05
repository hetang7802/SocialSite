from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html'),name ='login'),
    path('signup/',views.SignUp.as_view(),name = 'signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile_page/',views.MyProfileView.as_view(),name='profile_page'),

    path('update_profile/<slug>/',views.ProfileUpdateView.as_view(),name='update_profile'),
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset.html'),
        name="reset_password"),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_sent.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset_form.html'),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_rest_done.html"),
        name='password_reset_complete'),

    path('user_list/',
        views.users_list.as_view(),
        name = 'user_list'),

    path('friend_list/<slug>/',
        views.friend_list.as_view(template_name = 'accounts/friend_list.html'),
        name = 'friend_list'),

    path('users/<slug>/',
        views.user_profile.as_view(),
        name = 'user_profile'),

    path('users/friend-request/send/<int:id>',views.send_friend_request,
        name = 'send_friend_request'),

    path('users/friend-request/cancel/<int:id>',views.cancel_friend_request,
        name = 'cancel_friend_request'),

    path('users/friend-request/accept/<int:id>',views.accept_friend_request,
        name = 'accept_friend_request'),

    path('users/friend_request/decline/<int:id>',views.decline_friend_request,
        name = 'decline_friend_request'),

    path('users/delete_friend/<int:id>',views.delete_friend,name = 'delete_friend'),

    path('search_users/',views.search_users.as_view(),name = 'search_users'),

]
