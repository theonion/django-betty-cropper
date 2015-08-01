try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from django.conf import settings as _settings


BETTY_ADMIN_URL = urljoin(_settings.MEDIA_URL, "images/")
BETTY_IMAGE_URL = urljoin(_settings.MEDIA_URL, "images/")
BETTY_PUBLIC_TOKEN = None
BETTY_PRIVATE_TOKEN = None
BETTY_DEFAULT_IMAGE = None
