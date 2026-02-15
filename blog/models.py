from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# TODO: не давать зарегистрироваться если такая почта уже есть
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_completed = models.BooleanField(default=False) 
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Telegram chat id"
    )

    def __str__(self):
        return self.user.username

from ckeditor_uploader.fields import RichTextUploadingField
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    body = RichTextUploadingField()
    created = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    excerpt = models.CharField('Краткое описание', max_length=300, blank=True)
    def save(self, *args, **kwargs):
        if not self.excerpt and self.body:
            # Удаляем HTML-теги и берем первые 300 символов
            import re
            clean_body = re.sub(r'<[^>]+>', '', self.body)
            self.excerpt = clean_body[:300] + '...' if len(clean_body) > 300 else clean_body
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

class Product(models.Model):
    # название услуги, ограничение на 200 символов
    name = models.CharField(max_length=200)
    # услуги, неограниченное число символов
    description = models.TextField()
    # цена может быть только положительной, Positive - в переводе с англ.- положительное
    price = models.PositiveIntegerField()
    # фото услуги, в атрибуте upload_to пишем в какую папку сохранять фото
    # blank=True null=True означает, что фото прикреплять необязательно
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # метод для строкового представления объекта, используется в админке
    # и для вывода результатов в консоль при тестировании
   
    recommendation = models.BooleanField('Рекомендуем', default=True)
    
    new_product = models.BooleanField(
        default=True, 
        verbose_name='Новинка'
    )
   
    
    CATEGORY_CHOICES = [
        ('it', 'IT-услуги'),
        ('design', 'Дизайн'),
        ('education', 'Обучение'),
        ('Salads', 'Салаты'),
        ('Side_dishes', 'Гарниры'),
        ('Flour_products', 'Мучные изделия'),
        ('Hot_dishes', 'Горячие блюда'),
        ('Milk_cheese_eggs', 'Молоко, сыр, яйца'),
        ('Chips_snacks', 'Чипсы, снеки'),
        ('Water_and_drinks', 'Вода и напитки'),
        ('Tea_coffee_cocoa', 'Чай, кофе, какао'),
        ('other', 'Другое')
    # добавить возможность выбирать категории в админке
    ]
    category = models.CharField(choices=CATEGORY_CHOICES, default='other', max_length=20)
    # 1302
    PRODUCT_TYPE_CHOICES = [
        ('service', 'Кухня'),
        ('physical', 'Товар'),
    ]

    product_type = models.CharField(
        choices=PRODUCT_TYPE_CHOICES,
        default='physical',
        max_length=20,
        verbose_name='Тип')
    sku = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name='Артикул'
    )
    stock = models.PositiveIntegerField(
        default=0, 
        verbose_name='Остаток на складе'
    ) 
    

    requires_shipping = models.BooleanField(
        default=False, 
        verbose_name='Требуется доставка'
    )
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    def __str__(self):
        return self.name
    def get_product_type_display_with_icon(self):
        if self.product_type == 'service':
            return 'Услуга'
        else:
            return 'Товар'
    
    @property
    def is_service(self):
        return self.product_type == 'service'
    
    @property
    def is_physical(self):
        return self.product_type == 'physical'
    
    @property
    def is_in_stock(self):
        """Проверка наличия на складе для товаров"""
        if self.is_physical:
            return self.stock > 0
        return True  # Услуги всегда доступны если is_available=True
from django.core.validators import MinValueValidator
# класс для записи на услугу
class CartItem(models.Model):
    # связываем услугу которую хотят заказать с пользователем,
    # чтобы нам было понятно кто именно оформляет заказ
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # связываем заказ с конкретной услугой
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # указываем дату и время записи на услугу
    booking_date = models.DateTimeField(verbose_name="Дата и время записи", help_text="Когда клиент хочет получить услугу",blank=True,  null=True  )
    notes = models.TextField(blank=True, null=True, verbose_name="Примечание", help_text="Дополнительные пожелания клиента")
    # количество повторений,если услуга периодическая, например тренировка 2 раза в неделю
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
         ('completed', 'Выполнена'),
         ('cancelled', 'Отменена')
    ]
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} на {self.booking_date}"
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    booking = models.ManyToManyField(CartItem, related_name="orders")
    PAYMENT_STATUS = [
        ('pending', 'Ожидает оплаты'),
         ('paid', 'Оплачен'),
         ('failed', 'Ошибка оплаты')
    ]   
    PAYMENT_METHODS = [
        ('online', 'Онлайн'),
         ('cash', 'Наличные'),
         ('card', 'Картой при получении')
    ]
    status_of_payment = models.CharField(choices=PAYMENT_STATUS, default='pending')
    method_of_payment = models.CharField(choices=PAYMENT_METHODS, default='online')
    total_amount = models.PositiveIntegerField()

    def __str__(self):
        return f"Заказ услуг номер {self.id}"
    



    
from django.utils.translation import gettext_lazy as _
class Slide(models.Model):
    title = models.CharField(_('Заголовок'), max_length=200)
    description = models.TextField(_('Описание'), max_length=500, blank=True)
    image = models.ImageField(_('Изображение'), upload_to='slides/')
    link = models.URLField(_('Ссылка'), blank=True, help_text=_('Ссылка при клике на слайд'))
    is_active = models.BooleanField(_('Активный'), default=True)
    show_title = models.BooleanField(_('Показывать заголовок'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    class Meta:
        verbose_name = _('Слайд')
        verbose_name_plural = _('Слайды')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title