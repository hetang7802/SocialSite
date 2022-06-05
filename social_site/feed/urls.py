from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url

app_name = 'feed'

urlpatterns = [
    path('',views.PostListView.as_view(),name='post_list_view'),
    path('post/<int:pk>/like',views.like,name='post_like'),
    path('post/new/',views.CreatePost.as_view(),name = 'create_post'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post_detail_view'),
    path('post/by/<slug>/',views.UserPostListView.as_view(),name='user_posts'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='post_delete'),
    path('post/<int:pk>/comment/',views.CommentView.as_view(),name='new_comment'),
    path('post/<int:pk>/comments/',views.PostCommentList.as_view(),name='post_comments'),
    path('post/search/',views.SearchPosts.as_view(),name='search_posts'),
]
