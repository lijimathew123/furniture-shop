from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class FurnitureCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class FurnitureProduct(models.Model):
    category = models.ForeignKey(FurnitureCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image =models.ImageField(upload_to='product_images/')
    stock = models.PositiveIntegerField(default=1)

   

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(FurnitureProduct, through='CartItem')

    

class CartItem(models.Model):
    product = models.ForeignKey(FurnitureProduct, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Order"
    
    
class Review(models.Model):
    product = models.ForeignKey(FurnitureProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Review by {self.user.username} on {self.date}"


class Promotion(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/',null = True,blank=True)

    def __str__(self):
        return self.title