# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressTagList',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(help_text='The title that is displayed above the tag list.', max_length=255, null=True, verbose_name='Titel', blank=True)),
            ],
            options={
                'verbose_name': 'Tag List Plugin',
                'verbose_name_plural': 'Tag List Plugins',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name or title of location, e.g. "Opera House".', max_length=255, null=True, verbose_name='Name', blank=True)),
                ('logo', easy_thumbnails.fields.ThumbnailerImageField(help_text='Image of location.', upload_to=b'djangocms_address/', null=True, verbose_name='Logo', blank=True)),
                ('description', tinymce.models.HTMLField(help_text='Description of the location, e.g. "World-famous opera house offering major productions, original decor & multilingual guided tours."', null=True, verbose_name='Beschreibung', blank=True)),
                ('external_link', models.URLField(help_text='A link that provides further information about the location, e.g. "http://www.wiener-staatsoper.at/".', null=True, verbose_name='External link', blank=True)),
                ('link_title', models.CharField(help_text='Title that is displayed and wrapped with either CMS page link or External link, e.g. "More information".', max_length=255, null=True, verbose_name='Link title', blank=True)),
                ('street', models.CharField(help_text='The street (and street number) the location is located at, e.g. "Opernring 2".', max_length=255, null=True, verbose_name='Street', blank=True)),
                ('zipcode', models.IntegerField(help_text='The zipcode of the city in which the location is located in, e.g. "1200"', null=True, verbose_name='Zipcode', blank=True)),
                ('city', models.CharField(help_text='The city the location is located in, e.g. "Vienna".', max_length=255, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(help_text='The state the location is situated in, e.g. "Vienna".', max_length=255, null=True, verbose_name='Status', blank=True)),
                ('country', models.CharField(help_text='The country the location is situated in, e.g. "Austria".', max_length=255, null=True, verbose_name='Country', blank=True)),
                ('formatted_address', models.CharField(help_text='The formatted address string, e.g. "Opernring 2, 1010 Vienna, Austria".', max_length=255, verbose_name='Formatted address', blank=True)),
                ('latitude', models.FloatField(help_text='The latitude of the location, e.g. 48.203493.', verbose_name='Latitude', blank=True)),
                ('longitude', models.FloatField(help_text='The longitude of the location, e.g. 16.369168.', verbose_name='Longitude', blank=True)),
                ('cms_link', models.ForeignKey(blank=True, to='cms.Page', help_text='A link to a page on this website, e.g. "/oper-information/".', null=True, verbose_name='CMS page link')),
                ('sites', models.ManyToManyField(help_text='Location is associated with a certain site.', to='sites.Site', null=True, verbose_name='Site', blank=True)),
            ],
            options={
                'verbose_name': 'Standort',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='LocationsList',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(help_text='The title that is displayed above the location list.', max_length=255, null=True, verbose_name='Titel', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of a tag, e.g. "Music", which allow for customized grouping or filtering.', max_length=255, verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='tags',
            field=models.ManyToManyField(help_text='Tags of the location, e.g. "Music", which allow for customized grouping or filtering.', to='djangocms_address.Tag', null=True, verbose_name='Tags', blank=True),
        ),
    ]
