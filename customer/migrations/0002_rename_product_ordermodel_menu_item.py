# Generated by Django 4.2 on 2023-04-07 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordermodel',
            old_name='product',
            new_name='menu_item',
        ),
    ]
