from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Тестирование отправки email через Яндекс'
    
    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email для отправки теста')
    
    def handle(self, *args, **options):
        recipient_email = options['email']
        
        self.stdout.write("=" * 50)
        self.stdout.write("НАСТРОЙКИ EMAIL:")
        self.stdout.write(f"HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write("=" * 50)
        
        try:
            self.stdout.write(f"Отправка тестового письма на {recipient_email}...")
            
            send_mail(
                subject='Тест отправки email из Django',
                message='Поздравляем! Если вы видите это письмо, значит email работает корректно!\n\nЭто тестовое сообщение от вашего Django приложения.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            
            self.stdout.write(self.style.SUCCESS('✓ Письмо успешно отправлено!'))
            self.stdout.write(self.style.WARNING('⚠ Проверьте папку "Входящие" и "Спам" в Яндекс Почте'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR('✗ Ошибка отправки:'))
            self.stdout.write(f"   {type(e).__name__}: {e}")
            self.stdout.write("\nВОЗМОЖНЫЕ ПРИЧИНЫ:")
            self.stdout.write("1. Неправильный пароль приложения")
            self.stdout.write("2. Двухфакторная аутентификация не включена")
            self.stdout.write("3. Блокировка со стороны Яндекса")
            self.stdout.write("4. Неправильные настройки порта/шифрования")