# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='deal_type',
            field=models.CharField(choices=[('promotion', 'Promotion'), ('conditional_offer', 'Conditional offer'), ('gift', 'Gift')], default='promotion', max_length=120, verbose_name='Deal type'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, upload_to='brands', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='deal_type',
            field=models.CharField(choices=[('promotion', 'Promotion'), ('conditional_offer', 'Conditional offer'), ('gift', 'Gift')], default='promotion', max_length=120, verbose_name='Deal type'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to='categories', verbose_name='Navigation image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='template_name',
            field=models.CharField(choices=[('filters_on_top', 'Filters on top'), ('default', 'Filters on side'), ('fullwidht_filters_on_top', 'Fullwidth filters on top'), ('only_price_range_filter', 'Only price range filter')], default='filters_on_top', max_length=60, verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='categorycaracteristic',
            name='type',
            field=models.CharField(choices=[('choices', 'Choices'), ('boolean', 'Yes / No'), ('int', 'Numeric')], default='choices', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='deal_type',
            field=models.CharField(choices=[('promotion', 'Promotion'), ('conditional_offer', 'Conditional offer'), ('gift', 'Gift')], default='promotion', max_length=120, verbose_name='Deal type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='navimage',
            field=models.ImageField(null=True, upload_to='products/nav/', verbose_name='Navigation image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='products/qr/', verbose_name='Qr code'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slideshow_type',
            field=models.CharField(choices=[('jssor/slideshows/full_width_slider.html', 'Full width slider'), ('jssor/slideshows/banner_slider.html', 'Banner slider'), ('jssor/slideshows/bootstrap_slider.html', 'Bootstrap slider'), ('jssor/slideshows/images_gallery.html', 'Images gallery'), ('jssor/slideshows/bootstrap_modal.html', 'Bootstrap modal')], default='jssor/slideshows/bootstrap_slider.html', max_length=150, verbose_name='Slideshow type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='template_name',
            field=models.CharField(choices=[('default', 'Default'), ('fullwidth_slideshow', 'Fullwidth slideshow')], default='default', max_length=60, verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='products', verbose_name='Image'),
        ),
    ]
