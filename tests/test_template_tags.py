from django.template import Template, Context
from django.test import TestCase

from djbetty.conf import settings

from testproject.testapp.models import TestModel


class TemplateTagTestCase(TestCase):

    def test_image_js_template_tag(self):
        t = Template("{% load betty %}<script src=\"{% betty_js_url %}\"></script>")
        self.assertEquals(t.render(Context()), "<script src=\"//example.com/betty/image.js\"></script>")

    def test_cropped_template_tag(self):
        test_object = TestModel()
        test_object.listing_image.id = 12345
        t = Template("{% load betty %}{% cropped image %}")
        c = Context({"image": test_object.listing_image})
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/1234/5/16x9/600.jpg" />')

        t = Template('{% load betty %}{% cropped image width=900 ratio="16x9" format="png" %}')
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/1234/5/16x9/900.png" />')

    def test_cropped_bad_value(self):
        t = Template("{% load betty %}{% cropped image %}")
        c = Context({"image": ""})
        html = t.render(c)
        self.assertEqual(html, '<img src="http://example.com/betty/0/16x9/600.jpg" />')

    def test_cropped_url_template_tag(self):
        test_object = TestModel()
        test_object.listing_image.id = 12345
        t = Template('{% load betty %}<img src="{% cropped_url image %}" />')
        c = Context({"image": test_object.listing_image})
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/1234/5/16x9/600.jpg" />')

        t = Template('{% load betty %}<img src="{% cropped_url image width=900 ratio="1x1" format="png" %}" />')
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/1234/5/1x1/900.png" />')

    def test_image_id(self):
        t = Template('{% load betty %}<img src="{% cropped_url image %}" />')
        c = Context({"image": 12345})
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/1234/5/16x9/600.jpg" />')

        c = Context({"image": "12345"})
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/1234/5/16x9/600.jpg" />')

        c = Context({"image": ""})
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/0/16x9/600.jpg" />')

        c = Context({"image": None})
        self.assertEquals(t.render(c), '<img src="http://example.com/betty/0/16x9/600.jpg" />')

    def test_no_default_image(self):
        settings.BETTY_DEFAULT_IMAGE = None
        t = Template('{% load betty %}<img src="{% cropped_url image %}" />')

        c = Context({"image": None})
        self.assertEquals(t.render(c), '<img src="" />')

        c = Context({"image": ""})
        self.assertEquals(t.render(c), '<img src="" />')

        settings.BETTY_DEFAULT_IMAGE = 666
