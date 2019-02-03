from django.test import TestCase, Client
from memes.seed.factories import TemplateFactory
from .models import Meme


class MemeFormTestCase(TestCase):

    def setUp(self):
        self.og_full_data = {
            'top': 'hi top', 'bottom': 'hi bottom',
            'flavor': 'og'}
        self.c = Client()
        self.meme_template = TemplateFactory()

    def test_add_meme(self):
        meme_count = Meme.objects.count()
        response = self.c.post('/template/%s' % self.meme_template.slug,
                               self.og_full_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Meme.objects.count(), meme_count+1)
