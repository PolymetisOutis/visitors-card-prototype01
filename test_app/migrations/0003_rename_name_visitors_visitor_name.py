# Generated by Django 4.0.5 on 2022-06-08 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_rename_company_visitors_company_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitors',
            old_name='name',
            new_name='visitor_name',
        ),
    ]