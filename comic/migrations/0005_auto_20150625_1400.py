# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("comic", "0004_comicbook_unread")]

    operations = [
        migrations.CreateModel(
            name="ComicStatus",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("last_read_page", models.IntegerField()),
                ("unread", models.BooleanField()),
            ],
        ),
        migrations.RemoveField(model_name="comicbook", name="last_read_page"),
        migrations.RemoveField(model_name="comicbook", name="unread"),
        migrations.AddField(
            model_name="comicstatus",
            name="comic",
            field=models.ForeignKey(to="comic.ComicBook", on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name="comicstatus",
            name="user",
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
    ]
