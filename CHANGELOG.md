# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- GitHub Actions workflow publishing to PyPI via Trusted Publishing (OIDC)
  on release (`.github/workflows/publish.yml`).
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) running the test
  suite with coverage, Ruff (lint + format check) and mypy on Python 3.12,
  3.13 and 3.14 for pushes and pull requests to `master`.
- Real test suite for the `pages` app (36 tests covering models and MPTT tree
  behavior, slugify signals, URL routing, views and admin), replacing the
  placeholder `1 + 1 == 2` test.
- Ruff, mypy and coverage.py configuration in `pyproject.toml`, plus a `dev`
  dependency group (`coverage`, `mypy`, `ruff`).
- `Changelog` and `Issues` project URLs in the package metadata.

### Changed

- **Python**: dropped Python 2 and now require **Python 3.12+** (SPEC 0);
  tested on Python 3.14 and added the 3.14 trove classifier.
- **django-mptt**: constraint raised to `>=0.18` (resolves 0.18.0); Django
  stays on the **5.2 LTS** line (resolves 5.2.16).
- Removed legacy `# -*- coding: utf-8 -*-` declarations (redundant on
  Python 3) via Ruff's pyupgrade rules.
- **Django**: upgraded from Django 1.9 to **Django 5.2 LTS** (`>=5.2,<6.0`).
- Migrated packaging from `setup.py` + `requirements.txt` to a PEP 621
  `pyproject.toml` using the Hatchling build backend.
- Regenerated the initial migration against Django 5.2 / django-mptt 0.18
  (`BigAutoField` primary keys, current MPTT field definitions).
- Modernized the example project for Django 5.2 (`MIDDLEWARE`, `path()`/`re_path()`
  URLconf, removed deprecated settings).
- Rewrote `README.rst` with badges, a real `INSTALLED_APPS`/URLconf setup
  guide, `migrate` instructions (replacing the legacy `syncdb` reference)
  and development docs.
- Applied Ruff formatting and lint fixes across the code base (removed unused
  imports and legacy encoding comments; no behavior change).

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
- Fixed templates that failed to render on Django 5.2: replaced
  `{% load staticfiles %}` (removed in Django 3.0) with `{% load static %}`,
  replaced the `length_is` filter (removed in Django 5.1) with a
  `length == 0` comparison, added the missing module-level `register` to
  `pages/templatetags/menu.py` so `{% load menu %}` works, and guarded the
  breadcrumb section link so the index page renders without a section in
  context.

## [0.1.2] - 2016-05-04

Initial development version (never tagged or published to PyPI; the version
number comes from the original `pages/__init__.py` / `setup.py` metadata).

### Added

- `pages` reusable Django app with MPTT-backed `Page` and `Section` tree
  models, automatic slug generation via `pre_save` signals, Draft/Published/
  Hidden page statuses and active/public flags.
- Django admin integration for both models.
- Class-based views (`IndexView`, `SectionView`, `PageView`) with navigation
  mixins, URL patterns and SmartAdmin/Bootstrap-based templates and static
  assets.
- `example/` demo project (originally Django 1.9 / Python 2).
- MIT license.
