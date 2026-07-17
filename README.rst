django-boilerplate-pages
========================

|ci| |python| |django| |license|

.. |ci| image:: https://github.com/rangertaha/django-boilerplate-pages/actions/workflows/ci.yml/badge.svg?branch=master
   :target: https://github.com/rangertaha/django-boilerplate-pages/actions/workflows/ci.yml
   :alt: CI status

.. |python| image:: https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue
   :target: https://github.com/rangertaha/django-boilerplate-pages
   :alt: Supported Python versions

.. |django| image:: https://img.shields.io/badge/django-5.2%20LTS-0C4B33
   :target: https://www.djangoproject.com/
   :alt: Supported Django versions

.. |license| image:: https://img.shields.io/badge/license-MIT-green
   :target: https://github.com/rangertaha/django-boilerplate-pages/blob/master/LICENSE
   :alt: MIT License

A reusable Django app providing hierarchical **Pages** and **Sections**,
built on `django-mptt <https://github.com/django-mptt/django-mptt>`_.
Sections group pages into a site navigation tree, and pages themselves can
be nested, ordered, and toggled active/inactive. Both models are managed
through the Django admin.

Requires Python 3.12+ and Django 5.2 LTS.


Installation
------------

Install from a source checkout:

.. code-block:: bash

    pip install .

Usage
-----

Add ``mptt`` and ``pages`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "mptt",
        "pages",
    ]

Include the app's URLs in your project's ``urls.py``:

.. code-block:: python

    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("", include("pages.urls")),
    ]

Then create the database tables:

.. code-block:: bash

    python manage.py migrate

Create ``Section`` and ``Page`` records in the Django admin. Sections appear
at ``/<section-slug>``, top-level pages at ``/<section-slug>/<page-slug>``,
and nested pages at ``/<section-slug>/<parents>/<page-slug>``. Slugs are
generated automatically from the section name or page title when left blank.


Models
------

``Section``
    An MPTT tree of navigation sections. Each section has a name, slug,
    description, ordering, ``public``/``active`` flags, and a many-to-many
    relation to its pages (limited to active pages).

``Page``
    An MPTT tree of content pages with title, subtitle, description, body,
    ordering, an ``active`` flag, and a Draft/Published/Hidden status.


Example project
---------------

A demo project lives in ``example/``:

.. code-block:: bash

    cd example
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver


Development
-----------

Run the test suite from the example project:

.. code-block:: bash

    cd example
    python manage.py test pages

Lint and type-check:

.. code-block:: bash

    ruff check .
    ruff format --check .
    mypy


Known issues
------------

- ``pages/static/`` bundles a ~24 MB legacy SmartAdmin/Bootstrap theme,
  including a few demo ``.php`` files; it inflates the package and should
  eventually be trimmed or moved out of the app.
- ``pages/choices.py`` and ``pages/serializers.py`` are dead code — nothing
  imports them.
- The ``created``/``updated`` timestamp fields on ``Page`` and ``Section``
  have their ``auto_now``/``auto_now_add`` options swapped, so ``created``
  updates on every save and ``updated`` is set only on creation. Kept as-is
  for now because fixing it changes model/migration behavior.


License
-------

MIT — see the `LICENSE
<https://github.com/rangertaha/django-boilerplate-pages/blob/master/LICENSE>`_
file.
