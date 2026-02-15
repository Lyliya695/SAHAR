#Формы через Django упрощают создание форм, их валидацию (проверку)
from django import forms
#наша модель для комментариев
from .models import Comment
#встроенная форма для регистрации
from django.contrib.auth.forms import UserCreationForm
#встроенная модель пользователя
from django.contrib.auth.models import User


from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment #какая из наших моделей будет использоваться
        fields = ('body',)
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

from .models import Post
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','image', 'body','published']
# 1801





from .models import CartItem
class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['booking_date', 'notes', 'quantity']
        widgets = {
            'booking_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    # 1302

    def __init__(self, *args, **kwargs):
        # Извлекаем product из kwargs и удаляем его
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        # Если это товар (физический), скрываем поле booking_date
        if self.product and self.product.is_physical:
            # Убираем поле booking_date из формы
            if 'booking_date' in self.fields:
                del self.fields['booking_date']
      
# <input type="datetime-local">
# <textarea rows="3">


from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
# 0802-2
from .models import Slide

class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

# 1302
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'image', 
            'product_type', 'category',  
            'sku', 'stock', 'requires_shipping',   
            'is_available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'sku': forms.TextInput(attrs={'placeholder': 'Например: ART-001'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        product_type = cleaned_data.get('product_type')
        
        # Валидация для товаров
        if product_type == 'physical':
            if not cleaned_data.get('sku'):
                self.add_error('sku', 'Артикул обязателен для товаров')
            if not cleaned_data.get('stock'):
                self.add_error('stock', 'Укажите остаток на складе')
        

        return cleaned_data