from django.urls import path, include
from . import views
#подключение стандартных функций для входа/выхода
from django.contrib.auth import views as auth_views
from .views import login_view
from django.contrib.auth.views import LogoutView
from blog.views import ckeditor_upload_custom 
from ckeditor_uploader import views as ckeditor_views
app_name = 'blog'
from django.urls import reverse_lazy
#app_name=blog , 
# чтобы в HTML ссылаться на пути как blog:post_list
urlpatterns = [
    #главная страница, где посты блога будут отображаться
    #в файле views.py будет функция post_list
    path('',  views.service_list, name='service_list'),
    path('post/create_post/', views.create_post, name='create_post'),
    #страница конкретного поста (детальная)
path('post/<slug:slug>/', views.post_detail, name='post_detail'),
#для обработки лайков через AJAX
path('post/<slug:slug>/like/', views.like_post, name='like_post'),
#стандартные настройки для страницы входа, выхода и смены пароля

# path('accounts', include('django.contrib.auth.urls')),

# 0602 - 2 шаг
path('login/', views.login_view, name='login'),



path('logout/', views.logout_view, name='logout'),



path('register/', views.register, name='register'),
path('comment/<int:pk>/delete/', views.delete_comment, name="delete_comment"),
path('comment/<int:pk>/like/', views.like_comment, name="like_comment"),
path('profile/edit/', views.edit_profile, name="edit_profile"),
path('dashboard/', views.dashboard, name="dashboard"),
path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='blog/password_change.html',
             success_url='blog:password_change_done'
         ), 
         name='password_change'),
    
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='blog/password_change_done.html'
         ), 
         name='password_change_done'),

    #  новое, путь к каталогу услуг
    # path('catalog/', views.service_list, name='service_list'),

# новое, путь к конкретной услуге по ее АЙДИ (индивидуальному номеру из базы)
path('catalog/<int:product_id>/', views.service_detail, name='service_detail'),




# новое, путь к корзине, куда мы добавляем услугу
path('cart/', views.cart, name='cart'),
path('order/create/', views.create_order, name='create_order'),
# новое
path('ckeditor/browse/', ckeditor_views.browse, name='ckeditor_browse'),
path('ckeditor/upload/', ckeditor_upload_custom, name='ckeditor_upload'),
# 0802 - 1 шаг
   # URL для сброса пароля
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='blog/password_reset.html',
            email_template_name='blog/password_reset_email.html',
            subject_template_name='blog/password_reset_subject.txt',
            success_url=reverse_lazy('blog:password_reset_done')  
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='blog/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='blog/password_reset_confirm.html',
            success_url='/reset/done/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='blog/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


