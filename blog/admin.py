from django.contrib import admin
from .models import Post, Comment, Profile, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'published')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'active' )
    list_filter = ('active', 'created')
    actions = ['approve_comments']
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        # TODO: Вывод сообщений о успешной модерации нескольких комментариев одновременно
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Like)
# 1801
from .models import CartItem, Order
admin.site.register(CartItem)
admin.site.register(Order)

from django.contrib import admin





from .models import Slide
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title','show_title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active', 'order','show_title')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'show_title', 'description', 'image' )
        }),
        ('Настройки', {
            'fields': ('link', 'is_active', 'order')
        }),
    )

# python manage.py makemigrations
# python manage.py migrate

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'product_type', 'category', 'new_product', 'recommendation','price', 
        'is_available', 'stock_display'
    ]
    list_filter = ['product_type', 'category', 'is_available']
    search_fields = ['name', 'sku', 'description']
    list_editable = ['price', 'is_available', 'new_product', 'recommendation']
    def stock_display(self, obj):
        if obj.is_physical:
            return f"{obj.stock} шт."
        return "—"
    stock_display.short_description = "Остаток"
    # краткое описание
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price', 'image',
                        'is_available', 'new_product', 'recommendation')
        }),
        ('Тип и категория', {
            'fields': ('product_type', 'category')
        }),
        ('Для товаров', {
            'fields': ('sku', 'stock'),
            # поле можно свернуть
            'classes': ('collapse',),
            'description': 'Заполните только для физических товаров'
        }),
    )