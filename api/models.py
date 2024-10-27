from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='customer_profiles/', null=True, blank=True)


    def __str__(self):
        return self.user.username
    
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField()
    description = models.TextField(null=True, blank=True)
    cuisine_type = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='restaurant_profiles/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('Appetizer', 'Appetizer'),
        ('Salad', 'Salad'),
        ('Main Course', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Beverage', 'Beverage'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField(default="Ingredients not specified")  # New field for ingredients
    image = models.URLField(blank=True, null=True)  # New field for dish image URL
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Main Course')  # Category selection

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.dish.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.postal_code}, {self.country}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    DELIVERY_OPTION = [
        ('pickup', 'pickup'),
        ('delivery', 'delivery')
    ]

    ORDER_DELIVERY_STATUS = [
        ('order received','order received'),
        ('preparing','preparing'),
        ('on the way','on the way'),
        ('pick up ready','pick up ready'),
        ('delivered','delivered'),
        ('picked up','picked up')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # items = models.ManyToManyField(Cart)
    items = models.JSONField(default=list)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')  # Track order status
    delivery_option = models.CharField(max_length=20, choices=DELIVERY_OPTION, default='delivery')
    order_delivery_status = models.CharField(max_length=20, choices=ORDER_DELIVERY_STATUS, default='order received')

    # New field to store the restaurant associated with the order
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def get_ordered_items(self):
        return [{'dish_name': item.dish.name, 'quantity': item.quantity, 'price': item.dish.price} for item in self.items.all()]
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.order_status}"


