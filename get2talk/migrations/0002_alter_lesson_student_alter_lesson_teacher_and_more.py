# Generated by Django 4.2 on 2023-06-06 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('get2talk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='get2talk.student'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='get2talk.teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='get2talk.teacher'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=2000)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('reviewed', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
