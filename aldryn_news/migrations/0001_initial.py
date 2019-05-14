# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime
import djangocms_text_ckeditor.fields
import filer.fields.image
import cms.models.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('filer', '0007_auto_20161016_1055'),
        ('cms', '0012_auto_20150607_2207'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name='Ordering')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(help_text='Auto-generated. Clean it to have it re-created. WARNING! Used in the URL. If changed, the URL will change. ', max_length=255, verbose_name='Slug', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_news.Category', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'aldryn_news_category_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestNewsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('latest_entries', models.PositiveSmallIntegerField(default=5, help_text='The number of latests entries to be displayed.')),
                ('type_list', models.CharField(default='full', max_length=255, verbose_name='Type of list', choices=[('full', 'Full list'), ('simple', 'Simple list')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publication_start', models.DateTimeField(default=datetime.datetime.now, help_text='Used in the URL. If changed, the URL will change.', verbose_name='Published Since')),
                ('publication_end', models.DateTimeField(null=True, verbose_name='Published Until', blank=True)),
                ('category', models.ForeignKey(blank=True, to='aldryn_news.Category', help_text='WARNING! Used in the URL. If changed, the URL will change.', null=True, verbose_name='Category')),
                ('content', cms.models.fields.PlaceholderField(slotname='blog_post_content', editable=False, to='cms.Placeholder', null=True)),
                ('key_visual', filer.fields.image.FilerImageField(verbose_name='Key Visual', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'ordering': ['-publication_start'],
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsLinksPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('news', models.ManyToManyField(to='aldryn_news.News', verbose_name='News')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='NewsTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.CharField(help_text='Auto-generated. Clean it to have it re-created. WARNING! Used in the URL. If changed, the URL will change. ', max_length=255, verbose_name='Slug', blank=True)),
                ('lead_in', djangocms_text_ckeditor.fields.HTMLField(help_text='Will be displayed in lists, and at the start of the detail page', verbose_name='Lead-in')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_news.News', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'aldryn_news_news_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='aldryn_news_taggeditem_tagged_items', verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='aldryn_news_taggeditem_items', to='aldryn_news.Tag')),
            ],
            options={
                'verbose_name': 'Tagged Item',
                'verbose_name_plural': 'Tagged Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_news.Tag', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'aldryn_news_tag_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tagtranslation',
            unique_together=set([('language_code', 'master'), ('slug', 'language_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='newstranslation',
            unique_together=set([('language_code', 'master'), ('slug', 'language_code')]),
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=taggit.managers.TaggableManager(to='aldryn_news.Tag', through='aldryn_news.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='latestnewsplugin',
            name='tags',
            field=models.ManyToManyField(help_text='Show only the news tagged with chosen tags.', to='taggit.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('language_code', 'master'), ('slug', 'language_code')]),
        ),
    ]
