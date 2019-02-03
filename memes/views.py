from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.template import loader
from memes.models import Template, Meme
from memes.forms import OGMemeForm, TwitMemeForm, TemplateForm
import logging
import json

from django.http import Http404


def templates_new(request):
    if request.POST:
        template_form = TemplateForm(request.POST, request.FILES)
        if template_form.is_valid():
            t = Template()

            print(request.POST)
            if request.POST['url']:
                t.import_image_from_url(request.POST['url'])
            else:
                t.image = request.FILES['image']

            t.name = request.POST['name']
            t.save()
            return HttpResponseRedirect(reverse(
                'template_detail', args=([str(t.slug)])))

    else:
        template_form = TemplateForm()

    context = {
        'template_form': template_form
    }
    template = loader.get_template('templates/new.html')
    return HttpResponse(template.render(context, request))


def templates(request):
    all_templates = Template.objects.all()
    paginator = Paginator(all_templates, 24)
    page = request.GET.get('page')
    meme_templates = paginator.get_page(page)
    template = loader.get_template('templates/templates.html')

    context = {
        'templates': meme_templates,
    }
    return HttpResponse(template.render(context, request))


def memes(request):
    all_items = Meme.objects.all()
    paginator = Paginator(all_items, 24)
    page = request.GET.get('page')
    paginated_items = paginator.get_page(page)
    template = loader.get_template('memes/memes.html')

    context = {
        'memes': paginated_items
    }
    return HttpResponse(template.render(context, request))


def meme_details(request, slug):
    item = Meme.objects.get(slug=slug)
    recent_memes = Meme.objects.filter(
        template__slug=item.template.slug
    ).order_by('-modified_date')[0:10]
    template = loader.get_template('memes/details.html')

    context = {
        'meme': item,
        'recent_memes': recent_memes,
    }
    return HttpResponse(template.render(context, request))


def template_details(request, slug):
    meme_template = Template.objects.get(slug=slug)
    template = loader.get_template('templates/details.html')

    recent_memes = Meme.objects.filter(template__slug=slug)[0:10]

    if (request.method == 'POST') and ('flavor' not in request.POST):
        logging.error("Missing flavor from meme post")
        return HttpResponse("Missing meme flavor", status=500)

    if (request.method == 'POST') and ('flavor' in request.POST):
        if request.POST['flavor'] == 'og':
            og_form = OGMemeForm(request.POST)
            if og_form.is_valid():
                meme_template = Template.objects.get(slug=slug)

                data = {
                    'top': request.POST['top'],
                    'bottom': request.POST['bottom'],
                }
                m = Meme(
                    data=json.dumps(data),
                    template=meme_template,
                    flavor='og'
                )
                m.save()
        elif request.POST['flavor'] == 'twit':
            twit_form = TwitMemeForm(request.POST)
            if twit_form.is_valid():
                meme_template = Template.objects.get(slug=slug)

                data = {
                    'text': request.POST['text'],
                }
                m = Meme(
                    data=json.dumps(data),
                    template=meme_template,
                    flavor='twit'
                )
                m.save()

#   if (request.method == 'POST') and (request.POST['meme-type'] == 'og'):
#           og_form = OGMemeForm(request.POST)
#           if og_form.is_valid():
#               meme_template = Template.objects.get(slug=slug)
#               og_meme = og_form.save(commit=False)
#               og_meme.top = request.POST['top']
#               og_meme.bottom = request.POST['bottom']
#               og_meme.template = meme_template
#               og_meme.save()
#   else:
#       og_form = OGMemeForm()

#   if (request.method == 'POST') and (request.POST['meme-type'] == 'twit'):
#           twit_form = TwitMemeForm(request.POST)
#           if twit_form.is_valid():
#               meme_template = Template.objects.get(slug=slug)
#               twit_meme = twit_form.save(commit=False)
#               twit_meme.text = request.POST['text']
#               twit_meme.template = meme_template
#               twit_meme.save()
#   else:
#       twit_form = TwitMemeForm()

    og_form = OGMemeForm()
    twit_form = TwitMemeForm()
    context = {
        'og_form': og_form,
        'twit_form': twit_form,
        'recent_memes': recent_memes,
        'template': meme_template
    }
    return HttpResponse(template.render(context, request))


def adhoc_twit(request, slug, text):
        try:
            t = Template.objects.get(slug=slug)
        except Template.DoesNotExist:
            raise Http404("Template with slug '%s' does not exist" % slug)

        return_i = t.make_twit(text)
        response = HttpResponse(content_type="image/png")
        return_i.save(response, "PNG")
        return response

#       return HttpResponse(return_i.make_blob(),
#                           content_type=return_i.mimetype)


def adhoc_meme(request, slug, top, bottom):
        try:
            t = Template.objects.get(slug=slug)
        except Template.DoesNotExist:
            raise Http404("Template with slug '%s' does not exist" % slug)

        return_i = t.make_og_meme(top, bottom)

        return HttpResponse(return_i.make_blob(),
                            content_type=return_i.mimetype)
