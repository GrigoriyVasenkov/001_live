import datetime

import jwt as jwt
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from live import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, date_birthday, gender, **extra_fields):
        if not email:
            raise ValueError('Не заполненое поле Email')
        if not first_name:
            raise ValueError('Не заполненое поле Имя')
        if not last_name:
            raise ValueError('Не заполненое поле Фамилия')
        if not date_birthday:
            raise ValueError('Не заполненое поле Дата рождения')
        if not gender:
            raise ValueError('Не заполненое поле Пол')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, date_birthday=date_birthday, gender=gender **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):

    VOLUNTEER = 'Волонтер'
    ORGANIZER = 'Организатор'
    STATUS_CHOICES = [
        (VOLUNTEER, 'Волонтер'),
        (ORGANIZER, 'Организатор'),
    ]

    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='Фамилия'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Персонал'
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    date_birthday = models.DateTimeField(
        verbose_name='Дата рождения'
    )
    gender = models.CharField(
        max_length=7,
        verbose_name='Пол'
    )
    info = models.TextField(
        blank=True,
        verbose_name='Личная информация'
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        verbose_name='Телефон'
    )
    telegram_url = models.CharField(
        max_length=256,
        null=True,
        verbose_name='Telegram URL'
    )
    vk_url = models.CharField(
        max_length=256,
        null=True,
        verbose_name='VK URL'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=VOLUNTEER,
        verbose_name='Статус'
    )
    avatar_url = models.CharField(
        max_length=256,
        default='img/profile.png',
        verbose_name='Аватар URL'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_birthday', 'gender']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.datetime.now() + datetime.timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.get_full_name()} <{self.email}>'


class Organization(models.Model):

    full_name = models.CharField(
        max_length=256,
        verbose_name='Полное наименование'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    email = models.EmailField(
        max_length=256,
        verbose_name='Электронная почта'
    )
    address = models.CharField(
        max_length=256,
        verbose_name='Адрес'
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Телефон'
    )
    avatar_url = models.CharField(
        max_length=256,
        verbose_name='Аватар URL'
    )
    website = models.CharField(
        max_length=256,
        verbose_name='Сайт Организации'
    )
    legal_form = models.CharField(
        max_length=256,
        verbose_name='Организационно-правовая форма',
        db_index=True
    )
    leader = models.ForeignKey(
        User,
        related_name='organizations',
        on_delete=models.SET_NULL,
        verbose_name='Руководитель'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование',
        # для ускоренной сортировки
        db_index=True
    )
    full_name = models.CharField(
        max_length=256,
        verbose_name='Полное наименование',
        db_index=True
    )
    website = models.CharField(
        max_length=256,
        verbose_name='Сайт Проекта',
        db_index=True
    )
    material_url = models.CharField(
        max_length=256,
        verbose_name='Материал'
    )
    avatar_url = models.CharField(
        max_length=256,
        verbose_name='Аватар URL'
    )
    status = models.CharField(
        max_length=256,
        verbose_name='Статус проекта'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    goal = models.TextField(
        verbose_name='Цели'
    )
    result = models.TextField(
        verbose_name='Результаты'
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        db_index=True, verbose_name='Ссылка проекта'
    )
    organization = models.ForeignKey(
        Organization,
        related_name='projects',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Организация'
    )
    user = models.ManyToManyField(
        User,
        related_name='projects',
        through='UserProject',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Наименование события'
    )
    status = models.CharField(
        max_length=256,
        verbose_name='Статус мероприятия'
    )
    avatar_url = models.CharField(
        max_length=256,
        verbose_name='Аватар URL'
    )
    description = models.TextField(
        verbose_name='Описание события'
    )
    date_start = models.DateTimeField(
        verbose_name='Дата начала'
    )
    date_end = models.DateTimeField(
        verbose_name='Дата завершения'
    )
    contact_user = models.ForeignKey(
        User,
        related_name='events',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Контактное лицо'
    )
    project = models.ForeignKey(
        Project,
        related_name='events',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Проект'
    )
    client = models.ManyToManyField(
        User,
        related_name='events',
        through='ClientEvent',
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        db_index=True, verbose_name='Ссылка события'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    def __str__(self):
        return self.name


class Function(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Наименование'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    task = models.TextField(
        verbose_name='Задачи'
    )
    condition = models.TextField(
        verbose_name='Условия'
    )
    event = models.ForeignKey(
        Event,
        related_name='functions',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Событие'
    )
    client = models.ManyToManyField(
        User,
        related_name='functions',
        through='ClientFunction',
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        db_index=True, verbose_name='Ссылка функции'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    def __str__(self):
        return self.name
