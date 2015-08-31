from rest_framework import serializers


class ImageFieldSerializer(serializers.Field):

    def to_representation(self, obj):
        if isinstance(obj, dict):
            data = {
                "id": obj.get("id"),
                "alt": obj.get("alt"),
                "caption": obj.get("caption")
            }
        else:
            if obj is None or obj.id is None:
                return None
            data = {
                "id": obj.id,
            }
            if obj.field.alt_field:
                data["alt"] = obj.alt
            if obj.field.caption_field:
                data["caption"] = obj.caption
        return data

    def to_internal_value(self, data):

        if data is not None and "id" in data:
            data["id"] = int(data["id"])
            return data
        return None
