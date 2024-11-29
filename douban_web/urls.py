"""douban_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from douban_app import views
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', views.index),
    path('',views.login_user),
    path('login/',views.login_user),
    path('logout/',views.logout_user),
    path('reset_password/', views.reset_password),
    path('top10/', views.top10),
    path('search/', views.search),
    path('settings/', views.settings),
    path('help/', views.help),
    path('account/', views.account),
    path('signup/', views.signup),
    path('type_proportion/', views.type_proportion),
    path('avg_score/', views.avg_score),
    path('actor/', views.actor),
    path('film_total/', views.film_total),
    path('comments/<int:doubanId>/', views.comments),
    path('display/', views.display),
    path('score/<int:doubanId>/', views.user_score),
    path('score/<int:doubanId>/submit/', views.user_score_submit),
    path('favicon.ico', serve, {'path': 'img/favicon.ico'}),
    path('mail/active/', views.send_sms_code),
    path('user/sms_active/', views.sms_active),
    path('checkusername/',views.checkusername,name="checkusername"),
    path('checkpasswd/', views.checkpasswd,name="checkpasswd"),
    path('checkpasswdstrength/', views.checkPasswdStrength,name="checkpasswdstrength"),
    path('checkloginname/',views.checkloginname,name="checkloginname"),
    path('film/<int:doubanId>/',views.film_details),
    path('film/collect/<int:doubanId>/',views.film_collect),
    path('init/collect/<int:doubanId>/',views.init_collect),
    path('collect/',views.mycollect),
]
