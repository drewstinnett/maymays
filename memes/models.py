from django.db import models
from django.contrib import admin
from django.urls import reverse
import mimetypes
import requests
from django.core.files.base import ContentFile, File
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from io import BytesIO
from uuid import uuid4

# Needed for Meme gen
from PIL import Image as PILImage, ImageDraw, ImageFont
from textwrap import wrap
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color


class OGMeme(models.Model):
    """Original Gangsta' style meme.  Traditional top/bottom text on an image
    """
    top = models.CharField('Top Text', max_length=255, blank=True)
    bottom = models.CharField('Bottom Text', max_length=255, blank=True)
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ogmeme', blank=False, null=False)
    slug = models.SlugField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('meme_detail', args=[str(self.slug)])

    def __str__(self):  # pragma: no cover
        return "%s %s|%s" % (self.template.slug, self.top, self.bottom)

    def save(self, *args, **kwargs):
        i_blob = self.template.make_og_meme(self.top, self.bottom).make_blob()
        self.slug = "%s-%s" % (self.template.slug, uuid4())
        with BytesIO(i_blob) as stream:
            django_file = File(stream)
            self.image.save('%s.png' % self.template.slug, django_file,
                            save=False)

        super(OGMeme, self).save(*args, **kwargs)

    def import_image_from_url(self, url):
        r = requests.get(url)
        content_type = r.headers['content-type']
        ext = mimetypes.guess_extension(content_type)
        self.image.save('%s%s' % (self.slug, ext), ContentFile(r.content))

    def clean(self):
        if not self.top and not self.bottom:
            raise ValidationError('At least top or bottom text is required')

    class Meta:
        unique_together = ['top', 'bottom', 'template']
        ordering = ['-modified_date']


class Template(models.Model):
    """This is just a template for the various meme types.  Pretty much just an
    image and an identifire
    """

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to='templates', blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

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

    def get_absolute_url(self):
        return reverse('template_detail', args=[str(self.slug)])

    def make_twit(self, text, text_size=24, frame=10):
        """Generate a twit

        text_size: Font size for PIL
        frame: Number of pixels for the frame aroun final image
        """
        # Get the template for late use
        t = PILImage.open(self.image)

        # Figue out caption txt
        fnt = ImageFont.truetype('fonts/Metrophobic-Regular.ttf', text_size)
        ascent, descent = fnt.getmetrics()
        (width, baseline), (offset_x, offset_y) = fnt.font.getsize(text)
        font_height = offset_y + (ascent - offset_y) + descent
        text_pieces = wrap(text, self.image.width / 12)

        # Create image for the caption
        caption_height = (font_height * len(text_pieces)) + 10
        caption_i = PILImage.new(
            'RGB',
            (self.image.width, caption_height),
            color='white'
        )
        d = ImageDraw.Draw(caption_i)
        wrapped_text = "\n".join(text_pieces)
        d.text((10, 10), wrapped_text, fill='black', font=fnt)

        # Generate image to retun
        result = PILImage.new(
            "RGBA",
            (self.image.width + frame, (
                caption_height + self.image.height + (int(frame / 2)))),
            'white'
        )
        result.paste(caption_i, (int(frame / 2), 0))
        result.paste(t, (int(frame / 2), caption_height))

        return result

    def make_og_meme(self, top, bottom):
        """Generate an OG Meme
        """

        wand_t = Image(blob=self.image.read())
        MARGINS = [50, 130, 200, 270, 340]

        # Set a minimum size
        wand_t.resize(
            1024,
            int(
                (
                    (wand_t.height * 1.0) / (wand_t.width * 1.0)
                ) * 1024.0)
            )

        use_top = True
        use_bottom = True

        if top == ' ':
            use_top = False
        if bottom == ' ':
            use_bottom = False

        if use_top:
            upper_text = "\n".join(wrap(
                top, self.get_warp_length(int(wand_t.width)))).upper()
        if use_bottom:
            lower_text = "\n".join(wrap(
                bottom, self.get_warp_length(int(wand_t.width)))).upper()
            lower_margin = MARGINS[lower_text.count("\n")]

        text_draw = Drawing()

        text_draw.font = "fonts/Anton-Regular.ttf"
        text_draw.font_size = 70
        text_draw.text_alignment = "center"
        text_draw.stroke_color = Color("black")
        text_draw.stroke_width = 3
        text_draw.fill_color = Color("white")

        if use_top:
            text_draw.text(int(wand_t.width / 2), 80, upper_text)

        if use_bottom:
            text_draw.text(
                int(wand_t.width / 2), int(wand_t.height - lower_margin),
                lower_text)

        text_draw(wand_t)

        return(wand_t)

    def get_warp_length(self, width, max_width=1024, padding=33):
        return int((float(padding) / float(max_width)) * (width + 0.0))

    class Meta:
        ordering = ['name']

    def __str__(self):  # pragma: no cover
        return self.name


class TemplateAdmin(admin.ModelAdmin):
    pass


class OGMemeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Template, TemplateAdmin)
admin.site.register(OGMeme, OGMemeAdmin)
