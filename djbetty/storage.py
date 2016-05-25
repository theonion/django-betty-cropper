import requests

from django.core.files.storage import Storage

from djbetty.conf import settings


class BettyCropperStorage(Storage):

    def __init__(self, base_url=None, admin_url=None, public_token=None, private_token=None):
        self._admin_url = admin_url
        self._base_url = base_url
        self._public_token = public_token
        self._private_token = private_token

    @property
    def auth_headers(self):
        return {"X-Betty-Api-Key": self.public_token}

    @property
    def admin_url(self):
        base_url = self._admin_url
        if not base_url:
            base_url = settings.BETTY_ADMIN_URL
        if base_url.endswith("/"):
            base_url = base_url[:-1]

        return base_url

    @property
    def base_url(self):
        base_url = self._base_url
        if not base_url:
            base_url = settings.BETTY_IMAGE_URL
        if base_url.endswith("/"):
            base_url = base_url[:-1]

        return base_url

    @property
    def public_token(self):
        if self._public_token:
            return self._public_token
        return settings.BETTY_PUBLIC_TOKEN

    @property
    def private_token(self):
        if self._private_token:
            return self._private_token
        return settings.BETTY_PRIVATE_TOKEN

    def build_id_string(self, name):
        id_string = ""
        for index, char in enumerate(str(name)):
            if index % 4 == 0 and index != 0:
                id_string += "/"
            id_string += char

        return id_string

    def delete(self, image_id):
        raise NotImplementedError()

    def exists(self, image_id):
        detail_url = "{base_url}/api/{id}".format(base_url=self.admin_url, id=image_id)
        r = requests.get(detail_url, headers=self.auth_headers)
        return r.status_code == 200

    def listdir(self, path):
        raise NotImplementedError()

    def size(self, image_id):
        return 0

    def get_available_name(self, image_id):
        return image_id

    def build_base_url(self, fixed):
        base_url = getattr(settings, 'BETTY_FIXED_URL', None) if fixed else None
        if not base_url:
            base_url = self.base_url

        return base_url.rstrip('/')

    def _save(self, name, content):
        endpoint = "{base_url}/api/new".format(base_url=self.admin_url)

        data = {"name": name}
        files = {"image": content}

        r = requests.post(endpoint, files=files, headers=self.auth_headers)
        if r.status_code != 200:
            raise IOError("Save failed")

        return str(r.json()["id"])

    def url(self, name, ratio="original", width=600, format="jpg", fixed=False):
        return "{base_url}/{id_string}/{ratio}/{width}.{format}".format(
            base_url=self.build_base_url(fixed),
            id_string=self.build_id_string(name),
            ratio=ratio,
            width=width,
            format=format)

    def animated_url(self, name, format="gif", fixed=False):
        return "{base_url}/{id_string}/animated/original.{format}".format(
            base_url=self.build_base_url(fixed),
            id_string=self.build_id_string(name),
            format=format
        )
