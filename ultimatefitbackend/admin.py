from django.contrib import admin

# Register your models here.

from .models import Food, FoodCategory, FoodType, Order, Customer, Menu, MenuCategory, FoodOrder, Cart, GeneralPromotion, GroupPromotion, GroupPromotionFoodTypes, CouponPromotion, DeliveryOrder, AddressBook

from copy import deepcopy


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
    list_display = ('food_type', 'menu', 'convertdate_from_menu', 'price_from_foodtype', 'stock')


def add_multiple_food_object(modeladmin, request, queryset):
    print "Hello Worlf"

add_multiple_food_object.short_description = "Add multiple food object"


class FoodInline(admin.TabularInline):
    #list_display = ('food_type', 'category', 'price_from_foodtype','stock')
    readonly_fields = ('category', 'price_from_foodtype')
    fields = ('food_type', readonly_fields, 'stock')
    #exclude = ['order', 'foodcategory']
    model = Food
    # Change to extra = 1 (without makemigrations to see it easier)
    extra = 0


class FoodTypeAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'cols': '5',
        }

    list_display = ('name', 'price_lean', 'price_maintain', 'price_heavy')
    fields = (
        'name',
        'name_vn',
        'image',
        'price_lean', 
        'price_maintain', 
        'price_heavy', 
        ('cal_lean', 'protein_lean', 'carb_lean', 'fat_lean'),
        ('cal_maintain', 'protein_maintain', 'carb_maintain', 'fat_maintain'),
        ('cal_heavy', 'protein_heavy', 'carb_heavy', 'fat_heavy'),
        'available_categories',
        'discount_price'
    )


class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'food', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active', 'order_date')


def duplicate_menu(modeladmin, request, queryset):
    for menu in queryset:
        new_obj = deepcopy(menu)
        new_obj.id = None
        new_obj.save()

        # Copy each food object that belongs to this menu
        for food in Food.objects.filter(menu=menu):
            food_copy = deepcopy(food)
            food_copy.id = None
            food_copy.save()
            new_obj.food_set.add(food_copy)

            '''for choice in question.choices.all():
                choice_copy = deepcopy(choice)
                choice_copy.id = None
                choice_copy.save()
                question_copy.choices.add(choice_copy)'''

        new_obj.save()

duplicate_menu.short_description = "Duplicate Selected Menus"


class MenuAdmin(admin.ModelAdmin):
    model = Menu
    list_display = ('name', 'convertdate')
    #filter_horizontal = ('food_item',)
    inlines = (FoodInline,)
    actions = [duplicate_menu]


class GeneralPromotionAdmin(admin.ModelAdmin):
    class Media:
        # Have to put jquery before all js file in order to use jquery in the following js files
        js = (
            'ultimatefitbackend/js/jquery-2.1.4.js',
            'ultimatefitbackend/js/jquery-ui.min.js',
            'ultimatefitbackend/fullcalendar/lib/moment.min.js', 
            'ultimatefitbackend/js/admin_general_promotion.js',
        )

    list_display = ('name', 'percentage', 'startDate', 'endDate')


class GroupPromotionFoodTypesAdmin(admin.ModelAdmin):
    list_display = ('food_type', 'group_promotion')


class GroupPromotionFoodTypesInline(admin.TabularInline):
    fields = ('food_type',)
    model = GroupPromotionFoodTypes
    extra = 0


class GroupPromotionAdmin(admin.ModelAdmin):
    # class Media:
    #     js = (
    #         'ultimatefitbackend/js/jquery-2.1.4.js',
    #         'ultimatefitbackend/js/jquery-ui.min.js',
    #         'ultimatefitbackend/fullcalendar/lib/moment.min.js', 
    #         'ultimatefitbackend/js/admin_general_promotion.js',
    #     )

    list_display = ('name', 'percentage', 'startDate', 'endDate')
    inlines = (GroupPromotionFoodTypesInline,)


class CouponPromotionAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'ultimatefitbackend/js/jquery-2.1.4.js',
            'ultimatefitbackend/js/jquery-ui.min.js',
            'ultimatefitbackend/fullcalendar/lib/moment.min.js',
            'ultimatefitbackend/js/admin_coupon_promotion.js',
        )

    list_display = ('name', 'coupon_code', 'startDate', 'endDate', 'available_categories', 'percentage', 'percentage_with_cap', 'cap_percentage', 'absolute_with_min', 'min_absolute')
    fields = (
        'name',
        'coupon_code',
        'startDate',
        'endDate', 
        'available_categories',
        'percentage',
        ('percentage_with_cap', 'cap_percentage'),
        ('absolute_with_min', 'min_absolute')
    )


class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'order_data', 'user')


class AddressBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'first_name', 'last_name', 'address', 'city', 'email', 'phone_number')


admin.site.register(Food, FoodAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(FoodCategory)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuCategory)

admin.site.register(FoodOrder, FoodOrderAdmin)
admin.site.register(Cart, CartAdmin)

admin.site.register(DeliveryOrder, DeliveryOrderAdmin)
admin.site.register(AddressBook, AddressBookAdmin)

admin.site.register(GeneralPromotion, GeneralPromotionAdmin)
admin.site.register(GroupPromotion, GroupPromotionAdmin)
admin.site.register(GroupPromotionFoodTypes, GroupPromotionFoodTypesAdmin)
admin.site.register(CouponPromotion, CouponPromotionAdmin)