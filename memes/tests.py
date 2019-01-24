from django.test import TestCase, Client
from memes.models import Template, OGMeme
from memes.seed.factories import TemplateFactory
from memes.helpers import import_memes
from memes.forms import OGMemeForm
from django.core.files.base import ContentFile
from io import BytesIO
import json
from PIL import Image


def generate_image(width=500, height=500):
    size = (width, height)
    color = (255, 0, 0)
    i = Image.new("RGB", size, color)
    return i


class OGMemeFormTestCase(TestCase):

    def setUp(self):
        self.full_data = {'top': 'hi top', 'bottom': 'hi bottom'}
        self.c = Client()

        self.meme_template = TemplateFactory()
        fake_image = generate_image()
        i_buffer = BytesIO()

        fake_image.save(fp=i_buffer, format='JPEG')

        self.meme_template.image.save(
            'test.png', ContentFile(i_buffer.getvalue()))

    def test_add_meme(self):
        meme_count = OGMeme.objects.count()
        response = self.c.post('/template/%s' % self.meme_template.slug,
                               self.full_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OGMeme.objects.count(), meme_count+1)
#       self.assertTrue(b'"error": false' in response.content)

    def test_valid_meme(self):
        form = OGMemeForm(data=self.full_data)
        self.assertTrue(form.is_valid())

    def test_invalid_meme(self):
        form = OGMemeForm(data={'top': ' ', 'bottom': ' '})
        self.assertFalse(form.is_valid())

    def test_missing_bottom_meme(self):
        form = OGMemeForm(data={'top': 'Toponly Test', 'bottom': ' '})
        self.assertTrue(form.is_valid())

    def test_missing_top_meme(self):
        form = OGMemeForm(data={'top': ' ', 'bottom': 'Bottom only'})
        self.assertTrue(form.is_valid())


class ViewTemplatesTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.meme_template = TemplateFactory()
        fake_image = generate_image()
        i_buffer = BytesIO()

        fake_image.save(fp=i_buffer, format='JPEG')

        self.meme_template.image.save(
            'test.png', ContentFile(i_buffer.getvalue()))

    def test_template_listing(self):
        response = self.c.get('/templates/')
        self.assertEqual(response.status_code, 200)

    def test_template_details(self):
        response = self.c.get('/template/%s' % self.meme_template.slug)
        self.assertEqual(response.status_code, 200)


class ImportMemesTestCase(TestCase):
    def setUp(self):
        import_memes(silent=True, limit=15)

    def test_memes_imported(self):
        self.assertGreater(len(Template.objects.all()), 5)

    def test_kym_link(self):
        template = Template.objects.all()[0]
        self.assertIn('knowyourmeme', template.know_your_meme_url)


class AdHocTestCase(TestCase):

    def setUp(self):
        self.meme_template = TemplateFactory()

        fake_image = generate_image()
        i_buffer = BytesIO()

        fake_image.save(fp=i_buffer, format='JPEG')

        self.meme_template.image.save(
            'test.png', ContentFile(i_buffer.getvalue()))
        self.c = Client()

    def test_success_create(self):
        path = '/adhoc_meme/%s/top_text/bottom_text/' % self.meme_template.slug
        response = self.c.get(path)
        self.assertEqual(response.status_code, 200)

    def test_missing_create(self):
        path = '/adhoc_meme/NOTEXIST/top_text/bottom_text/'
        response = self.c.get(path)
        self.assertEqual(response.status_code, 404)


class GraphQLTestCase(TestCase):

    def setUp(self):
        Template.objects.create(name='Grumpy Cat')
        self._client = Client()

    def query(self, query: str, op_name: str = None, input: dict = None):
        '''
        Args:
            query (string) - GraphQL query to run

            op_name (string) - If the query is a mutation or named query, you
            must supply the op_name.  For annon queries ("{ ... }"), should be
            None (default).

            input (dict) - If provided, the $input variable in GraphQL will be
            set to this value

        Returns:

            dict, response from graphql endpoint.  The response has the "data"
            key.  It will have the "error" key if any error happened.

        '''
        body = {'query': query}
        if op_name:
            body['operation_name'] = op_name
        if input:
            body['variables'] = {'input': input}

        resp = self._client.post('/graphql', json.dumps(body),
                                 content_type='application/json')
        jresp = json.loads(resp.content.decode())
        return jresp

    def test_simple_query(self):
        resp = self.query('''
query{
  allTemplates{
    edges{
      node{
        name,
        slug
      }
    }
  }
}
''')
        self.assertNotIn('errors', resp, 'Response had errors')

    def test_simple_query_failure(self):
        resp = self.query('''queryxxx{ } ''')
        self.assertIn('errors', resp, 'Bad query id not produce errors')

    def test_graphsql_limit(self):
        TemplateFactory.create_batch(20)
        record_count = 3
        resp = self.query("""
query{
  allTemplates(first:%s){
    edges{
      node{
        name,
        slug
      }
    }
  }
}
""" % (record_count))
        self.assertEqual(len(resp['data']['allTemplates']['edges']),
                         record_count)
