# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_news import __version__

REQUIREMENTS = [
    'django-filer',
    'django-hvad',
    'django_select2>=5.11.1,<6',
    'django-taggit',
    'djangocms-text-ckeditor',
    'translitcodec',
    'Unidecode',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django :: 1.11',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-news',
    version=__version__,
    description='Publish news in django CMS',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/softformance/aldryn-news',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
