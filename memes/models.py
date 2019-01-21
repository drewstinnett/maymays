from django.db import models
from django.contrib import admin
import mimetypes
import requests
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError


class OGMeme(models.Model):
    """Original Gangsta' style meme.  Traditional top/bottom text on an image
    """
    top = models.CharField('Top Text', max_length=255, blank=True)
    bottom = models.CharField('Bottom Text', max_length=255, blank=True)
    template = models.ForeignKey('Template', on_delete=models.CASCADE)

    def clean(self):
        if not self.top and not self.bottom:
            raise ValidationError('At least top or bottom text is required')

    class Meta:
        unique_together = ['top', 'bottom', 'template']


class Template(models.Model):
    """This is just a template for the various meme types.  Pretty much just an
    image and an identifire
    """

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to='templates', blank=False, null=False)

    @property
    def know_your_meme_url(self):
        return "https://knowyourmeme.com/memes/%s" % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Template, self).save(*args, **kwargs)

    def import_image_from_url(self, url):
        r = requests.get(url)
        content_type = r.headers['content-type']
        ext = mimetypes.guess_extension(content_type)
        self.image.save('%s%s' % (self.slug, ext), ContentFile(r.content))

    def __str__(self):  # pragma: no cover
        return self.name


class TemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Template, TemplateAdmin)
