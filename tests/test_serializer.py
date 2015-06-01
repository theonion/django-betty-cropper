from django.test import TestCase

from testproject.testapp.models import TestModelSerializer, TestModel


class ImageSerializerTestCase(TestCase):

    def test_image_field(self):
        data = {
            "image": {
                "id": 3,
                "alt": "some alt",
                "caption": "some pig"
            }
        }
        serializer = TestModelSerializer(data=data)
        serializer.is_valid()
        test = serializer.save()
        assert test.id > 0
        assert test.image.id == 3
        assert test.image.alt == "some alt"
        assert test.image.caption == "some pig"

        # Now le't skill the caption/alt
        test.image.alt = None
        test.image.caption = None

        serializer = TestModelSerializer(test)
        assert serializer.data["image"] == {
            "id": 3,
            "alt": None,
            "caption": None
        }
        assert serializer.data["listing_image"] is None
