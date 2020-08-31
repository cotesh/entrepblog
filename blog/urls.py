from django.urls import path, include
from . import views
app_name = 'posts'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('create', views.post_create, name = 'post_create'),
    path('<slug:slug>', views.detail, name = 'detail'),
    path('<slug:slug>/edit', views.update, name = 'update'),
    path('<slug:slug>/delete', views.delete, name = 'delete'),
    # path('home', include('blog.urls')),
]
