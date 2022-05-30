# Generated by Django 3.2 on 2022-05-28 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0007_auto_20220528_1909'),
        ('events', '0011_auto_20220528_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='avatar_url',
            field=models.ImageField(default='event/avatars/profile.png', upload_to=events.models.Event.event_avatar_path, verbose_name='Аватар мероприятия'),
        ),
        migrations.AlterField(
            model_name='event',
            name='contact_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='users.user', verbose_name='Контактное лицо'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='event',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='projects.project', verbose_name='Проект'),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(max_length=256, verbose_name='Местоположение'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='function',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userfunction',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]