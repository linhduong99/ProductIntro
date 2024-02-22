from django.db import models
from django.conf import settings
from core.utils import slug_vi


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    ordinal = models.IntegerField(default=0, verbose_name='ordinal')
    image = models.ImageField(upload_to="media/categories")
    status = models.CharField(max_length=16, default=settings.COMMON_STATUS_PUBLISH,
                              choices=settings.COMMON_STATUS_CHOICES, verbose_name='status')
    
    def get_unique_slug(self):
        if self.title is None:
            return ''
        slug = slug_vi.slugify(self.title)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save()
        
    def __str__(self) -> str:
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    ordinal = models.IntegerField(default=0, verbose_name='ordinal')
    description = models.TextField(default="")
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=16, default=settings.COMMON_STATUS_PUBLISH,
                              choices=settings.COMMON_STATUS_CHOICES, verbose_name='status')
    
    def get_unique_slug(self):
        if self.name is None:
            return ''
        slug = slug_vi.slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save()
        
    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/products")
    ordinal = models.IntegerField(default=0, help_text='ordinal = 0 sẽ là ảnh to nhất')

    def __str__(self) -> str:
        return self.product.name


class Promotions(models.Model):
    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
        
    title = models.CharField(max_length=255, verbose_name='title')
    image = models.ImageField(upload_to="media/promotions")
    ordinal = models.IntegerField(default=0, verbose_name='ordinal')
    start_time = models.DateTimeField(null=False, blank=False, verbose_name='start_time')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='end_time')
    status = models.CharField(max_length=16, default=settings.COMMON_STATUS_DRAFT,
                              choices=settings.COMMON_STATUS_CHOICES, verbose_name='status')

    def __str__(self) -> str:
        return self.title
    