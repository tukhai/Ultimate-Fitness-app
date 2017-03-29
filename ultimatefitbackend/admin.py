from django.contrib import admin

# Register your models here.

from .models import Food, FoodCategory, Order, Customer, Menu, MenuCategory


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

#class FoodAdmin(admin.ModelAdmin):
#    list_display = ('title', 'price', 'stock')

    
admin.site.register(Food)
admin.site.register(FoodCategory)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(MenuCategory)


