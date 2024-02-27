from django.core.management.base import BaseCommand
import random

from Product.models import Product, ProductImage


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        product_images = ProductImage.objects.all()
        for pr in products:
            pr_ims = random.choices(product_images, k=random.choice([2,3,4]))
            for index, pr_im in enumerate(pr_ims):
                ProductImage.objects.create(
                    ordinal=index,
                    product=pr,
                    image=pr_im.image
                )
                
        # shuffle_products = list(products) * 15
        # random.shuffle(shuffle_products)
        # for index, pr in enumerate(shuffle_products):
        #     categories = pr.categories.all()
        #     instance = Product.objects.create(
        #         name=f"{pr.name}_{index}",
        #         slug=f"{pr.slug}_{index}",
        #         ordinal=index,
        #         short_description=pr.short_description,
        #         description=pr.description,
        #         status=pr.status,
        #     )
        #     instance.categories.set(categories)
            
        