from django.shortcuts import render, get_object_or_404, redirect
#декоратор для ограничения доступа, т.е. пока пользователь
#не зашел в аккаунт, то он не сможет лайкать посты, оставлять комментарии и т.д.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
#для ответов в формате JSON на AJAX
from django.contrib.auth import login 
#функция login для входа в аккаунт
from .models import Post, Like, Comment 
#наши модели Пост, Лайк и Комментарий
#TODO: добавить формы для комментариев и регистрации
from .forms import CommentForm, RegisterForm #наши формы из файла forms.py
#импорт форм для комментариев и регистрации
from django.contrib.auth.models import User
#импорт модели Пользователя
from django.contrib.auth.forms import UserCreationForm
#импорт стандартной формы для регистрации
from django.contrib import messages 
# модуль для вывода сообщений пользователю
from django.db.models import Q
# новое
from django.core.paginator import Paginator
from django.utils.text import slugify  # Добавь этот импорт в начале файла
import transliterate  # Нужно установить библиотеку
# pip install transliterate
# к услугам добавить пагинация

from .models import Slide
def post_list(request):
    posts = Post.objects.filter(published=True)
    #получаем из базы все посты, которые опубликованы
    #черновики игнорируем
    #третий аргумент - словарь, где хранятся данные доступные в HTML
    query = request.GET.get('q')
    # query = query.lower()
    # http://127.0.0.1:8000/?page=1
    # Поправить поиск с учетом регистра
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(body__icontains=query)
        )
    # новое
    paginator = Paginator(posts, 2)  # ← 2 поста на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    slides = Slide.objects.filter(is_active=True).order_by('order')

    return render(request, 'blog/post_list.html', {
        'posts': page_obj,
        'query': query,
        'page_obj': page_obj,
        'slides': slides,
    })
# Create your views here.
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    #пробуем найти пост по слагу, если его нет, то выдаем ошибку 404
    #проверяем, что пост опубликован
    comments = post.comments.filter(active=True) 
    #комментарии привязанные к конкретному посту, которые активны
    #TODO: обработка формы для нового комментария
    if request.method == 'POST':
        form = CommentForm(request.POST)
        #создаем экземпляр формы, передаем данные которые ввел пользователь
        #т.е. текст комментария
        if form.is_valid():
            #проверяем, что данные корректны, например, что комментарий не пустой
            comment = form.save(commit=False)
            #сохраняем текст комментария, но не в базу, а временно в переменную
            #зачем? чтобы привязать его к посту и к пользователю, а потом
            #сохранить в базу
            comment.post = post #привязываем комментарий к посту
            comment.author = request.user #привязываем комментарий к пользователю

            comment.save() #сохраняем в базу
            #возвращаем пользователя обратно, чтобы избежать
            #дублирования комментариев (повторной отправки формы)
            messages.success(request, "Ваш комментарий на модерации") 

            return redirect('blog:post_detail', slug=post.slug)
    else:
        #если GET-запрос, то создаем пустую форму (сбрасываем данные)
        form = CommentForm()
    return render(request, 'blog/post_detail.html', 
    {'post': post, 'comments': comments})


@login_required
#проверка на вход в аккаунт
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    user = request.user
    like, created = Like.objects.get_or_create(post=post, user=user)
    #функция get_or_create возвращает кортеж из 2 объектов
    #like - объект
    #created = True, если объект создан, False - если объект уже существует
    if not created:
        #если лайк уже стоял, то удаляем его
        like.delete()
        liked = False
    else:
        liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })

    return redirect('blog:post_detail', slug=slug)

#TODO: для формы регистрации
def register(request): #создаем метод для формы регистрации
    if request.method == 'POST': #если пользователь нажал на кнопку "зарегистрироваться"
        form = RegisterForm(request.POST) #получаем данные из формы
        if form.is_valid(): #если данные в форме корректны
            user = form.save() #сохраняем пользователя в базу
            login(request, user) #сразу выполняем за него вход
            #чтобы ему не пришлось это делать вручную
            return redirect('blog:edit_profile')
            #перенеправляем на главную страницу
    else: #иначе - если он просто зашел на страницу, форма должна быть пустой
        form = RegisterForm() #или если он повторно зашел
    #показываем страницу регистрации с пустой формой или с ошибками
    return render(request, 'blog/register.html', {'form': form})
# Функция для вывода сообщения после отправки формы и проверки данных
# TODO: забыли пароль
# TODO: телефон необязательным


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_slug = comment.post.slug
    comment.delete()
    return redirect('blog:post_detail', slug=post_slug)

@login_required #только для тех, кто вошел в аккаунт
def like_comment(request, pk): #добавляем функцию, т.е. возможность ставить лайки
    comment = get_object_or_404(Comment, pk=pk) #получаем комментарий на который
    # ставят лайк
    if request.user != comment.author: #если это чужой комментарий, не его
        if request.user in comment.likes.all(): #смотрим, он уже ставил лайк или нет?
            comment.likes.remove(request.user)
            liked = False #удаляем его лайк
        else: #если еще не ставил лайк
            comment.likes.add(request.user)
            liked = True #то добавляем его во множество
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': comment.likes.count()
        })
    
    return redirect('blog:post_detail', slug=comment.post.slug) 
    #возвращаемся на ту же самую страницу

from .forms import ProfileForm
@login_required
def edit_profile(request):
    profile = request.user.profile
    if profile.is_completed:
        return redirect('blog:dashboard')
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if request.FILES.get('avatar'):
                print("Имя файла:", request.FILES['avatar'].name)
            form.save()
            profile.is_completed = True 
            profile.refresh_from_db()
            print("ПУТЬ:", profile.avatar.path)
            return redirect('blog:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/edit_profile.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'blog/dashboard.html')
# 0802

from .forms import PostCreateForm

from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
@login_required
def create_post(request):
    # 1801
    if request.method=="POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # ИСПРАВЛЕННЫЙ КОД ДЛЯ СЛАГА:
            # 1. Берем заголовок
            title = post.title
            # 2. Переводим русские буквы в английские
            try:
                # Пробуем транслитерировать (если установлена библиотека)
                # title_translit = transliterate.translit(title, reversed=True)
                title_translit = transliterate.translit(title, reversed=True)
            except:
                # Если библиотеки нет или ошибка - используем заголовок как есть
                title_translit = title
            # 3. Создаем слаг
            # slugify автоматически: 
            # - переводит в нижний регистр
            # - заменяет пробелы на дефисы
            # - удаляет спецсимволы
            # - обрезает длину
            post.slug = slugify(title_translit)
            original_slug = post.slug
            counter = 1
            while Post.objects.filter(slug=post.slug).exists():
                post.slug = f"{original_slug}-{counter}"
                counter += 1
            post.save()
            return redirect('blog:dashboard')
        # TODO: выравнивание текста по левому краю, центру и правому
    else:
        form = PostCreateForm()
    return render(request, 'blog/create_post.html', {'form':form})

from .models import Order, CartItem, Product
def service_list(request):
    products = Product.objects.all()
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category=category)
    search = request.GET.get('search', '')     
    if search:
       products = products.filter(
           Q(name__icontains=search ) |
           Q(description__icontains=search)
       ) 
    categories = Product.CATEGORY_CHOICES

    slides = Slide.objects.filter(is_active=True).order_by('order')

    return render(request, 'blog/service_list.html', {
        'products':products,
        'slides': slides,
        'categories': categories,
        'selected_category': category,
        'search_query': search
    })

# def service_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'blog/service_detail.html', {
#         'product': product
#     })
# 1801










from .forms import CartItemForm
@login_required
def service_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, product=product)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.user = request.user
            cart_item.product = product

            if product.is_physical:
                cart_item.booking_date = None
            cart_item.save()
            if product.is_service:
                messages.success(request, 'Услуга добавлена в корзину!')
            else:
                messages.success(request, 'Товар добавлен в корзину!')
            return redirect('blog:cart')
    else:
        form = CartItemForm(product=product)
    return render(request, 'blog/service_detail.html', {
        'product': product,
        'form': form
    })

# 1801
@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user, status='pending')
    total = sum(item.total_price() for item in items)
    return render(request, 'blog/cart.html', {
        'items': items,
        'total': total
    })




@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user, status='pending')

    if not cart_items.exists():
        return redirect('blog:cart')

    total_amount = sum(item.total_price() for item in cart_items)
    for item  in cart_items:
        if item.product.is_physical:
            product = item.product
            product.stock -= item.quantity
            product.save()
              #  дописать условие

    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount
    )

    order.booking.set(cart_items)

    cart_items.update(status='confirmed')

    return render(request, 'blog/order_success.html', {
        'order': order
    })

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User

@csrf_exempt
def telegram_webhook(request):
    data = json.loads(request.body)

    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message["chat"]["id"]

    if text.startswith("/start"):
        parts = text.split()
        if len(parts) == 2:
            user_id = parts[1]
            try:
                user = User.objects.get(id=user_id)
                user.profile.telegram_chat_id = chat_id
                user.profile.save()
            except User.DoesNotExist:
                pass

    return HttpResponse("ok")
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ckeditor_uploader import views as ckeditor_views
from ckeditor_uploader.utils import storage, get_thumb_filename
from ckeditor_uploader.views import get_files_browse_urls, ImageUploadView
from django.http import JsonResponse
import os

@csrf_exempt
@login_required  # Только login_required, без проверки на staff
def ckeditor_upload_custom(request):
    """
    Кастомный view для загрузки файлов в CKEditor.
    Разрешает доступ всем аутентифицированным пользователям.
    """
    return ckeditor_views.upload(request)


# 0602 - 1 шаг
from .forms import CustomLoginForm  
def login_view(request):
    # Если пользователь уже авторизован, перенаправить на дашборд
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже вошли в систему')
        return redirect('blog:dashboard')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('blog:dashboard')
        else:
            messages.error(request, 'Неверный логин или пароль. Попробуйте снова.')
    else:
        form = CustomLoginForm()
    return render(request, 'blog/login.html', {'form': form})




from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('blog:service_list')  # или 'blog:login'

