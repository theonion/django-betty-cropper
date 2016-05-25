from __future__ import absolute_import

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:
    from urlparse import urlparse, urlunparse

from django import template
from django.template.loader import select_template

from djbetty.conf import settings
from djbetty.fields import ImageFieldFile, default_storage

register = template.Library()


class AnonymousImageField(object):

    def __init__(self, id):
        self.id = id
        self.storage = default_storage

    def get_crop_url(self, ratio="original", width=600, format="jpg", fixed=False):
        return self.storage.url(self.id, ratio=ratio, width=width, format=format, fixed=fixed)

    def get_animated_url(self, format="gif", fixed=False):
        return self.storage.animated_url(self.id, format=format, fixed=fixed)


def coerce_image(image):
    """For right now, we need to be able to pass a string, or an int, or None
    into the template tags, and still have them return something meaningful"""

    if not image:
        if hasattr(settings, 'BETTY_DEFAULT_IMAGE') and settings.BETTY_DEFAULT_IMAGE != None:
            # If we have a default image, let's use that.
            return AnonymousImageField(settings.BETTY_DEFAULT_IMAGE)
        else:
            return None

    if not isinstance(image, ImageFieldFile):
        # If this isn't an ImageField, coerce it
        try:
            image_id = int(image)
        except:
            if settings.BETTY_DEFAULT_IMAGE:
                image_id = settings.BETTY_DEFAULT_IMAGE
            else:
                return None
        image = AnonymousImageField(image_id)

    return image


@register.simple_tag
def cropped_url(image, ratio="16x9", width=600, format="jpg", fixed=False):
    image = coerce_image(image)
    if image is None:
        return ""

    return image.get_crop_url(ratio=ratio, width=width, format=format, fixed=fixed)


@register.simple_tag(takes_context=True)
def cropped(context, image, ratio="16x9", width=600, format="jpg", fixed=False):
    image = coerce_image(image)
    if not image or not image.id:
        if hasattr(settings, 'BETTY_DEFAULT_IMAGE'):
            image = AnonymousImageField(settings.BETTY_DEFAULT_IMAGE)
        else:
            return ""

    context["image"] = image
    context["image_url"] = image.get_crop_url(
        ratio=ratio, width=width, format=format, fixed=fixed
    )
    context["ratio"] = ratio
    context["width"] = width
    context["format"] = format

    t = select_template(["betty/cropped.html", "betty/cropped_default.html"])
    return t.render(context)


@register.simple_tag
def animated_url(image, format="gif", fixed=False):
    image = coerce_image(image)
    if image is None:
        return ""

    return image.get_animated_url(format=format, fixed=fixed)


@register.simple_tag
def betty_js_url():
    betty_image_url = settings.BETTY_IMAGE_URL
    # make the url protocol-relative
    url_parts = list(urlparse(betty_image_url))
    url_parts[0] = ""
    betty_image_url = urlunparse(url_parts)
    return "{}/image.js".format(betty_image_url)


@register.simple_tag
def betty_image_url():
    url = settings.BETTY_IMAGE_URL
    # make the url protocol-relative
    url_parts = list(urlparse(url))
    url_parts[0] = ""
    url = urlunparse(url_parts)
    return url


@register.simple_tag
def betty_fixed_url():
    url = settings.BETTY_FIXED_URL
    # make the url protocol-relative
    url_parts = list(urlparse(url))
    url_parts[0] = ""
    url = urlunparse(url_parts)
    return url
