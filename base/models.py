from django.db import models

from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category_items = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    # Discount fields
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def discounted_price(self):
        if self.discount_percentage > 0:
            discounted= self.price - (self.price * self.discount_percentage / 100)
            return round(discounted, 2)  # Rounds off to 2 decimal places

        return self.price

    def __str__(self):
        return self.name

class Pizza(MenuItem):
    SIZES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    size = models.CharField(max_length=1, choices=SIZES)
    toppings = models.ManyToManyField('Topping', blank=True)

class Topping(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Pasta(MenuItem):
    pass
