from django.db import models


class Project(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название проекта',
        # для ускоренной сортировки
        db_index=True
    )
    full_name = models.CharField(
        max_length=256,
        verbose_name='Полное наименование проекта',
        db_index=True
    )
    legal_form = models.CharField(
        max_length=256,
        verbose_name='Организационно-правовая форма',
        db_index=True
    )
    website = models.CharField(
        max_length=256,
        verbose_name='Сайт проета',
        db_index=True
    )
    material_url = models.CharField(
        max_length=256,
        verbose_name='Материал проекта'
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
        verbose_name='Описание проекта'
    )
    goal = models.TextField(
        verbose_name='Цели проета'
    )
    result = models.TextField(
        verbose_name='Результаты проекта'
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        db_index=True, verbose_name='Ссылка проекта'
    )
    organization_id = models.ForeignKey(
        Organization,
        related_name='projects',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Организация'
    )
    user_id = models.ManyToManyField(
        User,
        related_name='projects',
        through='UserProject',
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
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    user_id = models.ForeignKey(
        User,
        related_name='events',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Организация'
    )
    project_id = models.ForeignKey(
        Project,
        related_name='events',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Проект'
    )
    client_id = models.ManyToManyField(
        User,
        related_name='events',
        through='ClientEvent',
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        db_index=True, verbose_name='Ссылка события'
    )

    def __str__(self):
        return self.name


class Function(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Наименование функции'
    )
    description = models.TextField(
        verbose_name='Описание функции'
    )
    task = models.TextField(
        verbose_name='Задачи'
    )
    condition = models.TextField(
        verbose_name='Условия'
    )
    event_id = models.ForeignKey(
        Event,
        related_name='function',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Событие'
    )
    client_id = models.ManyToManyField(
        User,
        related_name='function',
        through='ClientFunction',
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        db_index=True, verbose_name='Ссылка функции'
    )

    def __str__(self):
        return self.name

