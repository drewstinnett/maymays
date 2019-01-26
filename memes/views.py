from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template import loader
from memes.models import Template, OGMeme
from memes.forms import OGMemeForm
from django.http import Http404


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
    all_items = OGMeme.objects.all()
    paginator = Paginator(all_items, 24)
    page = request.GET.get('page')
    paginated_items = paginator.get_page(page)
    template = loader.get_template('memes/memes.html')

    context = {
        'memes': paginated_items
    }
    return HttpResponse(template.render(context, request))


def meme_details(request, slug):
    item = OGMeme.objects.get(slug=slug)
    recent_items = OGMeme.objects.filter(
        template__slug=item.template.slug
    ).order_by('-modified_date')[0:10]
    template = loader.get_template('memes/details.html')

    context = {
        'meme': item,
        'recent_memes': recent_items
    }
    return HttpResponse(template.render(context, request))


def template_details(request, slug):
    meme_template = Template.objects.get(slug=slug)
    template = loader.get_template('templates/details.html')

    recent_memes = OGMeme.objects.filter(
        template__slug=slug).order_by('-modified_date')[0:10]

    if request.method == 'POST':
        og_form = OGMemeForm(request.POST)
        if og_form.is_valid():
            meme_template = Template.objects.get(slug=slug)
            og_meme = og_form.save(commit=False)
            og_meme.top = request.POST['top']
            og_meme.bottom = request.POST['bottom']
            og_meme.template = meme_template
            og_meme.save()
    else:
        og_form = OGMemeForm()

    context = {
        'og_form': og_form,
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
