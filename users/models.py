from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group as AuthGroup
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from utils.fields import TitleSlugField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    accepts_marketing = models.BooleanField(_('customer accepts marketing'), default=False)
    tax_exempt = models.BooleanField(_('customer is tax excempt'), default=False)
    company = models.CharField(_('company'), max_length=255, blank=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True)
    address1 = models.TextField(_('address'), blank=True)
    address2 = models.TextField(_("address con't"), blank=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    zip_code = models.CharField(_('postal / Zip code'), max_length=255, blank=True)
    country = CountryField(_('country'), blank=True)
    region = models.CharField(_('region'), max_length=255, blank=True)
    notes = models.TextField(_('notes'), help_text=_('Enter any extra notes relating to this customer.'), blank=True)
    tags = models.ManyToManyField('users.UserTag', help_text=_('Tags can be used to categorize customers into groups.'), blank=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        ordering = ('first_name',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        s = '{0} {1}'.format(self.first_name, self.last_name)
        return s.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserTag(models.Model):
    title = models.CharField(_('title'), max_length=255, unique=True)
    slug = TitleSlugField(_('slug'))
    updated = models.DateTimeField(_('updated'), auto_now=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.title


class Group(AuthGroup):
    class Meta:
        proxy = True
