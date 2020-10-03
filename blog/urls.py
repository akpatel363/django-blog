from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('post/<int:year>/<int:month>/<int:date>/<slug:slug>',
         views.PostDetail.as_view(), name="post_detail"),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(),
         name='post_list_by_tag'),
    path('search/', views.SearchView.as_view(), name="search")
]
