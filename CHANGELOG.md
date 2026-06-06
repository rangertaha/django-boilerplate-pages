# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- **Python**: dropped Python 2 and now require **Python 3.10+** (SPEC 0).
- **Django**: upgraded from Django 1.9 to **Django 5.2 LTS** (`>=5.2,<6.0`).
- **django-mptt**: upgraded to `>=0.16` (tested with 0.18).
- Migrated packaging from `setup.py` + `requirements.txt` to a PEP 621
  `pyproject.toml` using the Hatchling build backend.
- Regenerated the initial migration against Django 5.2 / django-mptt 0.18
  (`BigAutoField` primary keys, current MPTT field definitions).
- Modernized the example project for Django 5.2 (`MIDDLEWARE`, `path()`/`re_path()`
  URLconf, removed deprecated settings).

### Removed

- Dropped unused dependencies that were never imported by the code:
  `django-suit`, `django-admin-tools`, `django-mptt-admin`, `reportlab`,
  `PyPDF2`, `xhtml2pdf`, `markdown2`, `django-markdown-deux`, `nose`,
  `coverage`, `six`, `html5lib`, `httplib2`, `Pillow`.
- Removed the legacy `.travis.yml` CI config.

### Fixed

- Replaced Python 2 idioms and APIs removed in modern Django: implicit relative
  imports (`from models import *` → `from .models import *`), `__unicode__` →
  `__str__`, `ugettext_lazy` → `gettext_lazy`, `django.core.urlresolvers` →
  `django.urls`, `django.conf.urls.url` → `django.urls.re_path`,
  `super(Cls, self)` → `super()`, and removed `from __future__ import
  unicode_literals`.
- Added the now-required `on_delete=models.CASCADE` to the `TreeForeignKey`
  parent relations.
- Fixed an identity-vs-equality bug in the slugify signals
  (`slug is ''` → falsy check).
