"""ProductIntro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from Product.models import Product, Category


products_dict = {
    "queryset": Product.objects.all(),
    "date_field": "updated_at",
}

categories_dict = {
    "queryset": Category.objects.all(),
    "date_field": "updated_at",
}


urlpatterns = [
    path('admin/', admin.site.urls),
    # Text and xml static files:
    path('robots.txt', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    path('humans.txt', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),
    re_path(r'^_nested_admin/', include('nested_admin.urls')),
    path("", include("Product.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {
            "products": GenericSitemap(products_dict, priority=0.6),
            "categories": GenericSitemap(categories_dict, priority=0.6)
        }},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

