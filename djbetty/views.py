import json

from django.core.signing import TimestampSigner
from django.http import HttpResponse

from .conf import settings

signer = TimestampSigner(key=settings.BETTY_PRIVATE_TOKEN)


def authtoken(request):
    username = request.user.get_username()
    token = signer.sign(username)
    content = json.dumps({"token": token, "username": username})
    return HttpResponse(content, content_type="application/json")
