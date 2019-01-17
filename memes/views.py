from django.http import HttpResponse
from memes.models import Template
from django.http import Http404


# Needed for Meme gen
from textwrap import wrap
from memes.helpers import get_warp_length
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color

MARGINS = [50, 130, 200, 270, 340]


def adhoc_meme(request, slug, top, bottom):
        try:
            t = Template.objects.get(slug=slug)
        except Template.DoesNotExist:
            raise Http404("Template with slug '%s' does not exist" % slug)

        wand_t = Image(blob=t.image.read())

        # Set a minimum size
        wand_t.resize(
            1024,
            int(
                (
                    (wand_t.height * 1.0) / (wand_t.width * 1.0)
                ) * 1024.0)
            )

        upper_text = "\n".join(wrap(
            top, get_warp_length(int(wand_t.width)))).upper()
        lower_text = "\n".join(wrap(
            bottom, get_warp_length(int(wand_t.width)))).upper()
        lower_margin = MARGINS[lower_text.count("\n")]

        text_draw = Drawing()

        text_draw.font = "fonts/impact.ttf"
        text_draw.font_size = 70
        text_draw.text_alignment = "center"
        text_draw.stroke_color = Color("black")
        text_draw.stroke_width = 3
        text_draw.fill_color = Color("white")
        text_draw.text(int(wand_t.width / 2), 80, upper_text)
        text_draw.text(
            int(wand_t.width / 2), int(wand_t.height - lower_margin),
            lower_text)

        text_draw(wand_t)

        return HttpResponse(wand_t.make_blob(), content_type=wand_t.mimetype)
