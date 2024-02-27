from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('lien-he', views.contact),
    path("danh-muc-san-pham/<str:category>", views.list_products_by_category),
    path("san-pham/<str:product_slug>", views.get_product_detail),
]