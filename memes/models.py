from django.db import models
from django.contrib import admin
import mimetypes
import requests
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify


class Template(models.Model):
    """This is just a template for the various meme types.  Pretty much just an
    image and an identifire
    """

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to='templates', blank=False, null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Template, self).save(*args, **kwargs)

    def import_image_from_url(self, url):
        r = requests.get(url)
        content_type = r.headers['content-type']
        ext = mimetypes.guess_extension(content_type)
        self.image.save('%s%s' % (self.name, ext), ContentFile(r.content))

    def __str__(self):  # pragma: no cover
        return self.name


class TemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Template, TemplateAdmin)
