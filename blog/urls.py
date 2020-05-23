from django.urls import path
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<str:post>',
         views.PostDetailView.as_view(), name='post_detail'),
    path('<pk>/share/', views.PostShareView.as_view(), name='post_share'),
    path('tag/<str:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.PostSearchView.as_view(), name='post_search'),
]
