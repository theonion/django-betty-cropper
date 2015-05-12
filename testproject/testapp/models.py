from django.db import models

from djbetty.fields import ImageField
from djbetty.serializers import ImageFieldSerializer

from rest_framework import serializers


class TestModel(models.Model):

    image_caption = models.CharField(max_length=255, null=True, blank=True)
    image_alt = models.CharField(max_length=255, null=True, blank=True)

    listing_image = ImageField(null=True, blank=True)
    image = ImageField(alt_field="image_alt", caption_field="image_caption", null=True, blank=True)


class TestModelSerializer(serializers.ModelSerializer):

    ImageFieldSerializer(allow_null=True, read_only=True)

    class Meta:
        model = TestModel
