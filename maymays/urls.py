"""maymays URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from graphene_django.views import GraphQLView
from memes import views

urlpatterns = [
    # Just plain home
    path(r'', views.templates, name='home'),

    # Get that admin sun
    path('admin/', admin.site.urls),

    # Mmm, delicious API
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),

    # Ad-hocs
    path(r'adhoc_meme/<str:slug>/<top>/<bottom>/',
         views.adhoc_meme),
    path(r'adhoc_twit/<str:slug>/<text>', views.adhoc_twit),

    path(r'templates/', views.templates, name='templates'),
    path(r'templates/new', views.templates_new, name='templates'),
    path(r'memes/', views.memes, name='memes'),
    path(r'meme/<str:slug>', views.meme_details, name='meme_detail'),
    path(r'template/<str:slug>', views.template_details,
         name='template_detail')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
