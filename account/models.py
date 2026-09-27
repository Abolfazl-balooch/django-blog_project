from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر'
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='نام خانوادگی')
    bio = models.TextField(max_length=500, blank=True, verbose_name='بیوگرافی')
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, verbose_name='تصویر پروفایل'
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب های کاربری'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()