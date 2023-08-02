from django.db.models.signals import post_save, pre_delete, post_delete
from django.shortcuts import redirect
from django.conf import settings
from django.dispatch import receiver
from .models import Group, TelegramUser
from .tgApp import create_group, update_group, leave_group


@receiver(post_save, sender=Group)
def create_or_update_handler(sender, instance, **kwargs):
    group: Group = instance
    user_ids = [user.tguser_id for user in instance.users.all()]

    if group.chat_id is not None:
        update_group(group.chat_id, user_ids)
    else:
        photo_url = str(settings.BASE_DIR) + str(group.photo.url)
        chat = create_group(
            group.name, group.first_post, user_ids, photo_url)
        group.chat_id = chat.id
        group.save()


@receiver(pre_delete, sender=Group)
def leave_handler(sender, instance, using, origin, **kwargs):
    group: Group = instance
    user_ids = [
        user.tguser_id for user in group.users.filter(
            is_staff=True
        ).all()
    ]

    is_deleted = leave_group(group.chat_id, user_ids)

    if is_deleted:
        print("Telegram Gruppamizdan chiqildi Va O'chirildi")
    return redirect()
