from django.contrib import admin

# Register your models here.

from .models import Food, FoodCategory, FoodType, Order, Customer, Menu, MenuCategory, FoodOrder, Cart


'''class ChoiceInline(admin.TabularInline):
    model = Food
    extra = 3'''

'''class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']'''

'''class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    # list_display = ('name')
    # list_filter = ['pub_date']
    # search_fields = ['question_text']'''

class FoodAdmin(admin.ModelAdmin):
    #list_display = ('name', 'price', 'stock')
    list_display = ('food_type', 'menu', 'convertdate', 'stock')


class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('food', 'cart', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date')


class MenuAdmin(admin.ModelAdmin):
    model = Menu
    #filter_horizontal = ('food_item',)

    
admin.site.register(Food, FoodAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(FoodCategory)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuCategory)

admin.site.register(FoodOrder, FoodOrderAdmin)
admin.site.register(Cart, CartAdmin)


