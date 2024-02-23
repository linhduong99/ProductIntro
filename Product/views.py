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


def _get_list_categories_count_product(request):
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
            'title': ca.title,
            'photo_url': build_media_url(request=request, media_file=ca.image),
            'num_of_product': num_of_product
        }
        data.append(it)
    return data


def _get_product_data_from_products(request, products):
    product_ids = [pr.id for pr in products]
    product_images = ProductImage.objects.filter(product_id__in=product_ids).all().order_by('ordinal')
    data = []
    for pr in products:
        image_urls = []
        for pr_im in product_images:
            if pr_im.product_id != pr.id:
                continue
            image_urls.append(build_media_url(request=request, media_file=pr_im.image))
            
        data.append({
            'id': pr.id,
            'slug': pr.slug,
            'name': pr.name,
            'description': pr.description,
            'image': image_urls[0] if len(image_urls) > 0 else None,
            'images': image_urls
        })
    return data


def _get_list_products_paging(request):
    page_number = int(request.GET.get("page") or 1)
    # products = Product.objects.filter(
    #     status=settings.COMMON_STATUS_PUBLISH
    # ).all().order_by('ordinal')[(page_number-1)*PRODUCT_PAGE_LIMIT:page_number*PRODUCT_PAGE_LIMIT]
    
    query_products = Product.objects.filter(
        status=settings.COMMON_STATUS_PUBLISH
    ).all().order_by('ordinal')
    products = (list(query_products) * 10)[(page_number-1)*PRODUCT_PAGE_LIMIT:page_number*PRODUCT_PAGE_LIMIT]
    return _get_product_data_from_products(request=request, products=products)


def _get_list_product_by_category_slug(request, slug):
    # category = Category.objects.filter(slug=slug).first()
    page_number = int(request.GET.get("page") or 1)

    products = Product.objects.filter(categories__slug=slug).all()
    products = (list(products) * 20)[(page_number-1)*PRODUCT_PAGE_LIMIT:page_number*PRODUCT_PAGE_LIMIT]
    return _get_product_data_from_products(request=request, products=products)


def _get_list_categories(request):
    categories = Category.objects.all()
    data = []
    for ca in categories:
        it = {
            'id': ca.id,
            'ordinal': ca.ordinal,
            'slug': ca.slug,
            'title': ca.title,
            'photo_url': build_media_url(request=request, media_file=ca.image),
        }
        data.append(it)
    return data


def _get_related_product(request, product):
    categories = product.categories.all()
    related_products = Product.objects.filter(categories__in=categories).exclude(id=product.id).all()[:6]
    return _get_product_data_from_products(request=request, products=related_products)


def home(request):
    page = int(request.GET.get("page") or 1)
    # print("request.GET", request.__dict__)
    print("page", page)
    count_product = Product.objects.filter(status=settings.COMMON_STATUS_PUBLISH).count()
    num_of_page = int(40/PRODUCT_PAGE_LIMIT) + 1
    promotions = _get_promotions(request=request)
    categories = _get_list_categories_count_product(request=request)
    products = _get_list_products_paging(request=request)
    context = {
        'promotions': promotions,
        'categories': categories,
        'products': products,
        'page_obj': {
            'num_of_page': num_of_page,
            'page': page,
            'previous': f"?page={str(page - 1)}" if page > 1 else "#",
            'next': f"?page={str(page + 1)}" if page < num_of_page else "#",
            'has_next': page < num_of_page,
            'has_previous': page > 1
        }
    }
    # print("products", products)
    return render(request, "home/index.html", {'data': context})


def list_products_by_category(request, category):
    page = int(request.GET.get("page", 1)) 
    # category = request.GET.get("category")
    main_category = Category.objects.filter(slug=category).first()
    products = _get_list_product_by_category_slug(request=request, slug=category)
    num_of_page = int(40/PRODUCT_PAGE_LIMIT) + 1
    categories = _get_list_categories(request=request)
    related_categories = [ca for ca in categories if ca['id'] != main_category.id]
    
    data = {
        'category_title': main_category.title,
        'products': products,
        'related_categories': related_categories,
        'categories': categories,
        'page_obj': {
            'num_of_page': num_of_page,
            'page': page,
            'previous': f"?page={str(page - 1)}" if page > 1 else "#",
            'next': f"?page={str(page + 1)}" if page < num_of_page else "#",
            'has_next': page < num_of_page,
            'has_previous': page > 1
        }
    }
    return render(request, "home/products_list.html", {'data': data})


def get_product_detail(request, product_slug):
    categories = _get_list_categories(request=request)
    product = Product.objects.filter(slug=product_slug).first()
    products = _get_product_data_from_products(request=request, products=[product])
    related_products = _get_related_product(request, product)
    data = {
        **products[0],
        'related_products': related_products,
        'categories': categories,
    }
    return render(request, "home/product_detail.html", {'data': data})


def contact(request):
    categories = _get_list_categories(request=request)
    data = {
        'categories': categories
    }
    return render(request, "home/contact.html", {'data': data})
    