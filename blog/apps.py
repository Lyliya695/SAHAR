from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    default_auto_field = 'django.db.models.BigAutoField'
    # Явно указываем тип данных автоинкрементного поля
    #Автоинкремент - айди поля, которое автоматически каждый раз увеличивается на 1
    #то есть вы добавляете новый элемент в таблицу и у него ID само увеличивается на 1
    def ready(self):
        import blog.signals

