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

class Supplier(models.Model):
    name = models.CharField(max_length=50)
    mobileno = models.CharField(max_length=10)
    items = models.ManyToManyField(Item, related_name="suppliers")  # A supplier provides specific items

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=50)
    mobileno = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    item = models.ManyToManyField(Item)  # Change from ForeignKey to ManyToManyField
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return f"Order on {self.date}"
    

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