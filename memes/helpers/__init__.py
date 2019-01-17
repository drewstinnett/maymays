import requests
from memes.models import Template


def get_warp_length(width):
    return int((33.0 / 1024.0) * (width + 0.0))


def import_memes(silent=None):
    for item in requests.get('https://api.imgflip.com/get_memes'
                             ).json()['data']['memes']:
        t, created = Template.objects.get_or_create(name=item['name'])
        if created:
            t.import_image_from_url(item['url'])
            t.save()
            if not silent:
                print("Imported %s" % t)  # pragma: no cover
