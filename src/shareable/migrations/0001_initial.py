# Generated by Django 2.2.5 on 2019-09-28 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shareable.fields
import shareable.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shareable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('password', shareable.fields.HashField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('shareable_type', models.CharField(choices=[('FILE', 'FILE'), ('URL', 'URL')], max_length=16)),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('views_counter', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expired_at', models.DateTimeField(default=shareable.utils.get_expired_at)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shareables', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='shareable',
            index=models.Index(fields=['shareable_type', 'user'], name='shareable_type_user_idx'),
        ),
        migrations.AddIndex(
            model_name='shareable',
            index=models.Index(fields=['uuid'], name='uuid_idx'),
        ),
    ]