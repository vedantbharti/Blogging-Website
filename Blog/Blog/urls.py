from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog_app.urls', namespace='blog_app')),
    url(r'^accounts/',include('accounts.urls', namespace='accounts')),
    url(r'^accounts/',include('django.contrib.auth.urls')),
]
