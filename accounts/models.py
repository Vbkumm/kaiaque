from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from markdown import markdown


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('Foto perfil', upload_to='img/user_avatar/', blank=True, null=True)
    profile_cover = models.ImageField('Cover profile', upload_to='img/user_cover/', blank=True, null=True)
    first_name = models.CharField('Nome',max_length=30, blank=True)
    last_name = models.CharField('Sobrenome',max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    bio = models.TextField('Biografia',max_length=500, blank=True)
    location = CountryField('Nacionalidade',blank_label='(países)', blank=True)
    email = models.CharField('E-mail', max_length=254)
    url = models.URLField('URL', blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    you_tube = models.URLField('YouTube', max_length=200, blank=True)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def get_bio_as_markdown(self):
        return mark_safe(markdown(self.bio, safe_mode='escape'))

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile', args=[str(self.user)])

    def __get__(self, instance, owner):
        return instance.__dict__[self.user]
