"""diplom2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from find import views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	path('admin/', admin.site.urls, name='admin'),
	path('', views.index),
	path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
	path('regis/', views.regis, name='regis'),
	path('post_missing/', views.post_missing),
    path('post_victim/', views.post_victim),
    path('posts/', views.PostList.as_view(template_name='posts.html')),
    path('thanks/', views.thanks, name='thanks'),
    path('image/', views.image),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post'),
    path('mypost/<int:pk>/', views.mypost, name='mypost')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)