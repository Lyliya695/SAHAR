








from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order
from .utils import send_telegram_message

@receiver(m2m_changed, sender=Order.booking.through)
def notify_new_order(sender, instance, action, **kwargs):
    # нас интересует момент, когда услуги УЖЕ добавлены
    if action != "post_add":
        return
    items = instance.booking.all()
    message = (
        f"🛒 <b>Новый заказ №{instance.id}</b>\n\n"
        f"👤 Клиент: {instance.user.username}\n"
        f"💰 Сумма: {instance.total_amount} ₽\n\n"
        f"<b>Услуги:</b>\n"
    )

    for item in items:
        message += (
            f"▫️ {item.product.name}\n"
            f"🔢 Кол-во: {item.quantity}\n"
            f"💬 {item.notes or '—'}\n\n"
        )
        if item.product.is_service:
                    # Для услуг показываем дату, если она есть
            if item.booking_date:
                    message += f"{item.booking_date.strftime('%d.%m.%Y %H:%M')}\n"
        else:
                    # Для товаров показываем артикул
            if item.product.sku:
                message += f"  Артикул: {item.product.sku}\n"
    send_telegram_message(message)

from .models import Comment

@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, created, **kwargs):
    if not created:
        return

    message = (
        f"💬 <b>Новый комментарий</b>\n\n"
        f"👤 Автор: {instance.author.username}\n"
        f"📝 Пост: {instance.post.title}\n\n"
        f"{instance.body[:300]}"
    )

    send_telegram_message(message)
from .models import Post

@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):
    if not created or not instance.published:
        return

    message = (
        f"🆕 <b>Новый пост</b>\n\n"
        f"✍ Автор: {instance.author.username}\n"
        f"📌 {instance.title}"
    )

    send_telegram_message(message)


from .utils import send_telegram_to_user

@receiver(m2m_changed, sender=Order.booking.through)
def notify_new_order(sender, instance, action, **kwargs):
    if action != "post_add":
        return

    items = instance.booking.all()

    message = (
        f"🛒 <b>Ваш заказ №{instance.id} принят</b>\n\n"
        f"💰 Сумма: {instance.total_amount} ₽\n\n"
        f"<b>Услуги:</b>\n"
    )

    for item in items:
        message += f"▫️ {item.product.name}\n"

    send_telegram_to_user(instance.user, message)
