"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include # include для подключения маршрутов из приложений
#для доступа к настройкам проекта
from django.conf import settings
#для работы с медиафайлами в режиме разработки
from django.conf.urls.static import static

urlpatterns = [
    #путь к админ-панели
    path('admin', admin.site.urls),
    #путь ко всем маршрутам приложения blog, (примечание: после этого в папке blog создается файл urls.py
    path('', include('blog.urls', namespace='blog')),
    #namescape=blog , чтобы ссылаться на пути как blog:post_list 
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#дополнительно для режима разработки    
#загруженные пользователями файлы, мы будет раздавать через URL (ссылки)

