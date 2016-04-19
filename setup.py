#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as r:
    req = r.read()

setup(
    name="django-boilerplate-pages",
    version=__import__('pages').get_version().replace(' ', '-'),
    url='https://github.com/rangertaha/django-boilerplate-pages',
    author='Rangertaha',
    author_email='rangertaha@gmail.com',
    description='',
    long_description=readme,
    packages=find_packages(exclude=['example', ]),
    include_package_data=True,
    install_requires=req,
    classifiers=[
        'Framework :: Django',
    ],
)
