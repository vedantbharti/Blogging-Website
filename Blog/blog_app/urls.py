from django.conf.urls import url
from blog_app import views
from django.urls import path

app_name = 'blog_app'

urlpatterns = [
    url(r'^$', views.PostListView.as_view(),name='post_list'),
    url(r'^about/$', views.AboutView.as_view(),name='about'),
    url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(),name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.as_view(),name='new_post'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.UpdatePostView.as_view(),name='edit_post'),
    url(r'^drafts/$', views.DraftListView.as_view(),name='draft_post_list'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.DeletePostView.as_view(),name='delete_post'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    path('search/', views.SearchResultView.as_view(),name='search_results'),

]
