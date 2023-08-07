# Generated by Django 4.2.3 on 2023-08-07 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'оплата', 'verbose_name_plural': 'оплаты'},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='paid_lesson',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='payment',
            name='id_payment_intent',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='id намерения платежа'),
        ),
        migrations.AddField(
            model_name='payment',
            name='id_payment_method',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='id метода платежа'),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Оплачено'),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='статус платежа'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='сумма оплаты'),
        ),
    ]
