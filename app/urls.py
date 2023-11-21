from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('blog/<slug:slug>', views.blog, name="read"),
    path('subscribe', views.subscribe, name='subscribe'),
    path('more', views.load_more_posts, name='more'),
    path('comment/<slug:slug>', views.comment, name='comment')
]
