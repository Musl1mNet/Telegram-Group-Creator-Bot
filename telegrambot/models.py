from django.db import models
from config.validators import PhoneValidator
from telegrambot.tgApp import get_tgusers, create_group


class TelegramUser(models.Model):
    gender_choices = (("Female", "Female"), ("Man", "Man"))
    tguser_id = models.BigIntegerField(default=None, null=True, blank=True)
    first_name = models.CharField(
        max_length=255, null=True, default=None, blank=True, verbose_name="Ism")
    last_name = models.CharField(
        max_length=255, null=True, default=None, blank=True, verbose_name="Familiya")
    username = models.CharField(
        max_length=255, null=True, default=None, blank=True, verbose_name="Tg foydalanuvchi nomi")
    phone = models.CharField(max_length=14, unique=True,
                             validators=[PhoneValidator()])
    gender = models.CharField(max_length=255, default=None,
                              null=True, choices=gender_choices, verbose_name="Jinsi")
    is_staff = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        users = get_tgusers('+' + self.phone).users
        user = users[0] if len(users) > 0 else None
        if user is not None:
            self.tguser_id = user.id
            if user.username:
                self.username = user.username
        super(TelegramUser, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.first_name


class Group(models.Model):
    chat_id = models.BigIntegerField(default=None, null=True, blank=True)
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(TelegramUser)
    first_post = models.CharField(max_length=255)
    photo = models.ImageField(
        upload_to="Group/", default="vatanparvar_logo.png", verbose_name="gruppa rasmi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Gruppa"
        verbose_name_plural = "Gruppalar"
