from django.contrib import admin

from customer_management.models import Customer
from users.models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','email','phone_number')
    search_fields = ('email','phone_number')

@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','fio','email','description')
    search_fields = ('fio','email')