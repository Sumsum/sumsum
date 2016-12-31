from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.postgres.fields import ArrayField
from django.core.mail import send_mail
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from metafields.models import MetaFieldsMixin
from utils.fields import ChoiceField, StringField, TextField, WysiwygField


STATE_CHOICES = (
    (None, ''),
    ('disabled', _('Disabled')),  # customers are disabled by default until they are invited. Staff accounts can disable a customer's account at any time.
    ('invited', _('Invited')),  # the customer has been emailed an invite to create an account that saves their customer settings.
    ('enabled', _('Enabled')),  # the customer accepted the email invite and created an account.
    ('declined', _('Declined')),  # the customer declined the email invite to create an account.
)


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


class User(MetaFieldsMixin, AbstractBaseUser, PermissionsMixin):
    accepts_marketing = models.BooleanField(_('customer accepts marketing'), default=False)
    bio = WysiwygField(_('biography'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    default_address = models.ForeignKey('customers.CustomerAddress', verbose_name=_('default address'), blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = StringField(_('first name'))
    homepage = models.URLField(_('homepage'), blank=True, null=True)
    last_name = StringField(_('last name'))
    multipass_identifier = StringField(_('multipass identifier'))
    note = TextField(_('notes'), help_text=_('Enter any extra notes relating to this customer.'))
    state = ChoiceField(_('state'), max_length=50, choices=STATE_CHOICES, required=False)  # maybe we need to sync this the is_active field
    tags = ArrayField(StringField(_('tag'), required=True), verbose_name=_('tags'), default=[])
    tax_exempt = models.BooleanField(_('customer is tax excempt'), default=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    verified_email = models.BooleanField(_('verified email'), default=False)

    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        ordering = ('first_name',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return ' '.join(filter(None, [self.first_name, self.last_name]))

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @cached_property
    def account_owner(self):
        """
        https://help.shopify.com/themes/liquid/objects/article#article-user-account_owner
        Returns "true" if the author of the article is the account owner of the
        shop. Returns "false" if the author is not the account owner.
        """
        raise NotImplemented


class Group(AuthGroup):
    class Meta:
        proxy = True
