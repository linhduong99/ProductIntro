import datetime
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q, Count
from core.usecases import build_media_url
from .models import Promotions, Product, Category, ProductImage


PRODUCT_PAGE_LIMIT = 12


def _get_promotions(request):
    dt_now = datetime.datetime.now()
    promotions = Promotions.objects.filter(
        Q(status=settings.COMMON_STATUS_PUBLISH)
        & Q(start_time__lte=dt_now)
        & Q(Q(end_time__isnull=True) | Q(end_time__gte=dt_now))
    ).order_by('ordinal')
    result = []
    for pr in promotions:
        it = {
            'id': pr.id,
            'ordinal': pr.ordinal,
            'photo_url': build_media_url(request=request, media_file=pr.image),
        }
        result.append(it)
    return result


def _get_list_categories(request):
    categories = Category.objects.filter(status=settings.COMMON_STATUS_PUBLISH).all().order_by('ordinal')
    count_products = Product.objects.all().values(
        'categories'
    ).annotate(
        count_products=Count('categories')
    )
    data = []
    for ca in categories:
        num_of_product = 0
        for cp in count_products:
            if cp['categories'] == ca.id:
                num_of_product = cp['count_products']
        it = {
            'id': ca.id,
            'ordinal': ca.ordinal,
            'slug': ca.slug,
            'photo_url': build_media_url(request=request, media_file=ca.image),
            'num_of_product': num_of_product
        }
        data.append(it)
    return data


def _get_list_products_paging(request):
    page_number = request.GET.get("page") or 1
    products = Product.objects.filter(
        status=settings.COMMON_STATUS_PUBLISH
    ).all().order_by('ordinal')[(page_number-1)*PRODUCT_PAGE_LIMIT:page_number*PRODUCT_PAGE_LIMIT]
    product_ids = [pr.id for pr in products]
    product_images = ProductImage.objects.filter(product_id__in=product_ids).all().order_by('ordinal')
    data = []
    for pr in products:
        images = []
        for pr_im in product_images:
            if pr_im.product_id != pr.id:
                continue
            images.append(build_media_url(request=request, media_file=pr_im.image))
            
        data.append({
            'id': pr.id,
            'slug': pr.slug,
            'name': pr.name,
            'description': pr.description,
            'images': images,
        })
    return data


def home(request):
    count_product = Product.objects.filter(status=settings.COMMON_STATUS_PUBLISH).count()
    promotions = _get_promotions(request=request)
    categories = _get_list_categories(request=request)
    products = _get_list_products_paging(request=request)
    context = {
        'promotions': promotions,
        'categories': categories,
        'products': products,
        'num_of_page': int(count_product/PRODUCT_PAGE_LIMIT) + 1
    }
    return render(request, "home/index.html", {'data': context})
