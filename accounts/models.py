# from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True, max_length=320, help_text='Provide an email for registration')
    name = models.CharField(_('Name'), max_length=70)

    # date_confirmation_mail_sent = models.DateTimeField(_('date confirmation mail sent'), default=timezone.now)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email