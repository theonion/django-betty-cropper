import os

from django.conf import settings

MODULE_ROOT = os.path.dirname(os.path.realpath(__file__))


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:"
            }
        },

        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.messages",
            "django.contrib.staticfiles",

            "testproject.testapp",
            "djbetty"
        ),
        TEMPLATE_LOADERS = (
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader"
        ),

        BETTY_IMAGE_URL="http://example.com/betty/",
        BETTY_PUBLIC_KEY="noop",
        BETTY_PRIVATE_KEY="noop",
        BETTY_DEFAULT_IMAGE=0
    )
