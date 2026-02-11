from __future__ import annotations

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import linebreaksbr as django_linebreaksbr
from django.urls import reverse


def environment(**options):
    """Jinja2 environment for Django.

    Keeps templates close to Django Template Language parity by exposing a few
    commonly-needed helpers/filters.
    """

    from jinja2 import Environment

    env = Environment(**options)

    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
        }
    )

    env.filters.update(
        {
            "linebreaksbr": django_linebreaksbr,
        }
    )

    return env
