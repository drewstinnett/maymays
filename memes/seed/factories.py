import factory
from faker import Factory
from memes.models import Template


faker = Factory.create()


class TemplateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Template

    name = factory.Sequence(lambda n: '{0} {1}'.format(faker.name(), n))
    print(name)
