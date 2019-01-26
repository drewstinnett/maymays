import factory
from faker import Factory
from memes.models import Template, OGMeme


faker = Factory.create()


class TemplateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Template

    name = factory.Sequence(lambda n: '{0} {1}'.format(faker.name(), n))
    image = factory.django.ImageField(color='green', width=200, height=300)


class OGMemeFactory(factory.DjangoModelFactory):
    class Meta:
        model = OGMeme

    top = factory.Sequence(lambda n: '{0} {1}'.format(faker.sentence(), n))
    bottom = factory.Sequence(lambda n: '{0} {1}'.format(faker.sentence(), n))
    template = factory.SubFactory(TemplateFactory)
