from graphene_django import DjangoObjectType
from memes.models import Template as TemplateModel
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.debug import DjangoDebug


class Template(DjangoObjectType):
    class Meta:
        model = TemplateModel
        filter_fields = {
            'name': ['exact', 'icontains'],
            'slug': ['exact']
        }
        interfaces = (graphene.relay.Node, )


class Query(object):
    debug = graphene.Field(DjangoDebug, name='__debug')
    template = graphene.relay.Node.Field(Template)
    all_templates = DjangoFilterConnectionField(Template)

#  def resolve_templates(self, info):
#       return TemplateModel.objects.all()
