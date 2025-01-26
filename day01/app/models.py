from django.db import models
from django.utils.timezone import now



# Create your models here.
class category (models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class unit (models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class Item (models.Model):
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length=255, default="-")
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    image = models.ImageField(upload_to = 'items')
    category = models.ForeignKey(category, on_delete = models.CASCADE)
    unit = models.ForeignKey(unit, on_delete = models.CASCADE)
   
    def __str__(self):
        return self.name

class Supplier (models.Model):
    name = models.CharField(max_length = 20)
    mobileno = models.CharField(max_length = 10)
    item = models.ManyToManyField(Item)
   
    def __str__(self):
        return self.name
    
class Order (models.Model):
    customer = models.CharField(max_length = 50)
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    item = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    def __str__(self):
        return self.customer
    

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Stationary', 'Stationary'),
        ('Beverages', 'Beverages'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    
class Cart(models.Model): 
    session_key = models.CharField(max_length=40, unique=True) 
    created_at = models.DateTimeField(default=now) 
    
    def get_total_price(self): 
        return sum(item.get_total_price() for item in self.items.all())
    
class CartItem(models.Model): 
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE) 
    product = models.ForeignKey(Item, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self): 
        return self.quantity * self.product.price 