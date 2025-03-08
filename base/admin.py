from django.contrib import admin
from .models import Category, MenuItem, Pizza, Pasta, Topping

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_percentage', 'discounted_price', 'category_items', 'is_available']
    list_filter = ['category_items', 'is_available']
    search_fields = ['name', 'category__name']
    readonly_fields = ['discounted_price']

    def discounted_price(self, obj):
        return obj.discounted_price()
    discounted_price.short_description = "Discounted Price"

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_percentage', 'discounted_price', 'size']
    list_filter = ['size']
    search_fields = ['name']

    def discounted_price(self, obj):
        return obj.discounted_price()
    discounted_price.short_description = "Discounted Price"

# @admin.register(Pasta)
# class PastaAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'discount_percentage', 'discounted_price']
#     search_fields = ['name']

#     def discounted_price(self, obj):
#         return obj.discounted_price()
#     discounted_price.short_description = "Discounted Price"

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['name']
