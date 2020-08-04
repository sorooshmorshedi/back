"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from helpers.views.TestView import TestView
from server import settings

...

# Create our schema's view w/ the get_schema_view() helper method. Pass in the proper Renderers for swagger
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
                  url('test', TestView.as_view()),

                  url(r'^home/', include('home.urls')),

                  url(r'^login$', obtain_auth_token, name='login'),
                  url(r'^users/', include('users.urls')),
                  url(r'^companies/', include('companies.urls')),
                  url(r'^accounts/', include('accounts.urls')),
                  url(r'^wares/', include('wares.urls')),
                  url(r'^sanads/', include('sanads.urls')),
                  url(r'^transactions/', include('transactions.urls')),
                  url(r'^cheques/', include('cheques.urls')),
                  url(r'^factors/', include('factors.urls')),
                  url(r'^reports/', include('reports.urls')),

                  url(r'^imprests/', include('imprests.urls')),

                  path('admin/', admin.site.urls),

                  url(r'^dashtbashi/', include('_dashtbashi.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
