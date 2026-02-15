# blog/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def staff_or_author_required(view_func):
    """
    Декоратор, который разрешает доступ:
    - staff пользователям
    - автору контента
    - всем аутентифицированным для CKEditor
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Доступ запрещен")
    return wrapper