# Generated by Django 4.0.3 on 2022-04-24 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_reviewproductrelation_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, null=True),
        ),
    ]
