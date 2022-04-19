# Generated by Django 3.2 on 2022-04-19 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="city",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="latitude",
            field=models.DecimalField(
                blank=True, decimal_places=16, max_digits=22, null=True
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="longitude",
            field=models.DecimalField(
                blank=True, decimal_places=16, max_digits=22, null=True
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="postcode",
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="street",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="street_number",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
