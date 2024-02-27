from django.contrib import admin
from django.urls import resolve
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.utils.html import format_html
from .models import *


admin.ModelAdmin.list_per_page = 50

TIME_FORMAT_DISPLAY = "%d/%m/%Y-%H:%M:%S"


def _display_img(url, icon, name):
    return format_html('''
                        <div class="overlay-image">
                            <a href="{}" target="_blank">
                             <img class="image" src="{}" style="width:64px" alt="" />
                             <div class="text">{}</div>
                            </a>
                        </div>
                        ''', url, icon, name[-40:])


def _display_audio(url, name):
    return format_html('''
                        <div class="overlay-image">
                            <audio controls>
                            <source src="{}"" type="audio/mpeg">
                            <source src="{}" type="audio/ogg">
                            </audio>
                            <a href="{}" target="_blank">
                                <div class="text">{}</div>
                            </a>
                        </div>
                        ''', url, url, url, name[-40:])


def _display_url(url, name):
    return format_html('''
                        <div class="overlay-image">
                            <a href="{}" target="_blank">{}</a>
                        </div>
                        ''', url, name[-20:])

class BaseAdmin(admin.ModelAdmin):
    save_as = True
    empty_value_display = '-'

    def lookup_allowed(self, lookup, *args, **kwargs):
        if str(lookup).endswith('idx'):
            return True
        return super().lookup_allowed(lookup, *args, **kwargs)

    def display_img_url(self, obj):
        if obj.image_url:
            return format_html('<a href="{}"><img src="/media/{}" style="width:100px" alt="" /> </a>', obj.image_url.url, obj.image_url)
        return ''

    display_img_url.short_description = 'Image'

    def display_icon_url(self, obj):
        if obj.icon_url:
            return format_html(u'<img src="/media/{}" style="width:100px" alt="" />', obj.icon_url)
        return ''

    display_icon_url.short_description = 'Icon'

    def display_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    display_content.short_description = 'Content'

    def created_time(self, obj):
        return obj.created_at.strftime(TIME_FORMAT_DISPLAY)

    created_time.admin_order_field = 'created_at'
    created_time.short_description = 'Created at'

    def updated_time(self, obj):
        return obj.updated_at.strftime(TIME_FORMAT_DISPLAY)

    updated_time.admin_order_field = 'updated_at'
    updated_time.short_description = 'Updated at'

    def display_id(self, obj):
        return obj.id

    display_id.admin_order_field = 'id'
    display_id.short_description = 'id'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('id',)
        return self.readonly_fields

    def valid_from_time(self, obj):
        if obj.valid_from:
            return obj.valid_from.strftime(TIME_FORMAT_DISPLAY)

    valid_from_time.admin_order_field = 'valid_from'
    valid_from_time.short_description = 'Valid from'

    def valid_to_time(self, obj):
        if obj.valid_to:
            return obj.valid_to.strftime(TIME_FORMAT_DISPLAY)

    valid_to_time.admin_order_field = 'valid_to'
    valid_to_time.short_description = 'Valid to'
    
    
class IdNestedTabularInlineBaseAdmin(NestedTabularInline):
    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.filter(id=int(resolved.kwargs['object_id'])).first()
        return None

    def has_add_permission(self, request, obj=None):
        parent = self.get_parent_object_from_request(request)
        if parent is not None and parent.status != settings.COMMON_STATUS_DRAFT:
            return request.user.is_superuser
        return True

    def has_delete_permission(self, request, obj=None):
        parent = self.get_parent_object_from_request(request)
        if parent is not None and parent.status != settings.COMMON_STATUS_DRAFT:
            return request.user.is_superuser
        return True

    def has_change_permission(self, request, obj=None):
        parent = self.get_parent_object_from_request(request)
        if parent is not None and parent.status != settings.COMMON_STATUS_DRAFT:
            return request.user.is_superuser
        return True


class ProductImageInline(IdNestedTabularInlineBaseAdmin):
    model = ProductImage
    extra = 0
    max_num = 10


@admin.register(Promotions)
class PromotionsAdmin(BaseAdmin):
    save_as = False
    
    def display_image(self, obj):
        if obj:
            if obj.image is not None:
                return _display_img(obj.image.url, obj.image.url, obj.image.name)
            return '-'
        return '-'

    display_image.short_description = "image"
    
    list_display = ('id', 'ordinal', 'title', 'start_time', 'end_time', 'status', 'display_image')
    readonly_fields = ('id',)
    
    
@admin.register(Product)
class ProductAdmin(BaseAdmin, NestedModelAdmin):
    save_as = False
    
    def display_categories(self, obj):
        if obj.categories:
            return ', '.join(obj.categories.all().values_list('title', flat=True))
        return '-'

    display_categories.admin_order_field = 'categories'
    
    list_display = ('id', 'name', 'ordinal', 'description', 'display_categories', 'status')
    readonly_fields = ('id',)
    search_fields = ['id', 'name']
    inlines = [ProductImageInline]
    
    
@admin.register(ProductImage)
class ProductImageAdmin(BaseAdmin):
    save_as = False
    
    def display_image(self, obj):
        if obj:
            if obj.image is not None:
                return _display_img(obj.image.url, obj.image.url, obj.image.name)
            return '-'
        return '-'

    display_image.short_description = "image"
    
    list_display = ('id', 'ordinal', 'product', 'display_image')
    readonly_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    save_as = False
    
    def display_image(self, obj):
        if obj:
            if obj.image is not None:
                return _display_img(obj.image.url, obj.image.url, obj.image.name)
            return '-'
        return '-'

    display_image.short_description = "image"

    
    list_display = ('id', 'title', 'ordinal', 'display_image', 'status')
    readonly_fields = ('id',)
    search_fields = ['id', 'title']
