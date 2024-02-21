from django.db import models


class Category(models.Model):
    class Meta:
        base_manager_name = "Category"
        
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to="categories")
    
    def __str__(self) -> str:
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(default="")
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")

    def __str__(self) -> str:
        return self.product.name


class Promotions(models.Model):
    image = models.ImageField(upload_to="promotions")