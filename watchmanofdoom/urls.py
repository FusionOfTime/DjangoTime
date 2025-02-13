"""
URL configuration for watchmanofdoom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from first import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page),
    path('time/', views.time_page),
    path('calc/', views.calc_page),
    path('expression/', views.expression_page),
    path('history/', views.history_page),
    path('delete/', views.delete_last_expression),
    path('clear/', views.clear_history),
    path('new/', views.new_expression),
    path('str2words/', views.str2words_page),
    path('str_history/', views.str_history_page),
    path('clicker/', views.clicker_page),
    path('save_stats/', views.save_stats),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
]
