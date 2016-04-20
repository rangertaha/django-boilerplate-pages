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
    license="The MIT License",
    keywords='django-boilerplate-pages',
    classifiers=[
         'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
