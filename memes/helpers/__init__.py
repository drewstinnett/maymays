import requests
from memes.models import Template


def import_memes(silent=None, limit=None):
    memes = requests.get(
        'https://api.imgflip.com/get_memes').json()['data']['memes']

    if limit:
        memes = memes[0:limit]

    for item in memes:
        t, created = Template.objects.get_or_create(name=item['name'])
        if created:
            t.import_image_from_url(item['url'])
            t.save()
            if not silent:
                print("Imported %s" % t)  # pragma: no cover
