# Generated by Django 5.0.3 on 2024-03-31 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_post_slug"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MarkdownContent",
        ),
    ]
