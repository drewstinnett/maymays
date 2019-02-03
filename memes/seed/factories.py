import factory
from faker import Factory
from memes.models import Template, Meme
import json


faker = Factory.create()


class TemplateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Template

    name = factory.Sequence(lambda n: '{0} {1}'.format(faker.name(), n))
    image = factory.django.ImageField(color='green', width=200, height=300)


def og_meme_seq(n):
    return json.dumps({
        'top': '%s %s' % (faker.sentence(), n),
        'bottom': '%s %s' % (faker.sentence(), n),
    })


class MemeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Meme

    data = factory.Sequence(og_meme_seq)
    flavor = 'og'
    template = factory.SubFactory(TemplateFactory)
