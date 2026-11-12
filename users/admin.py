from django.contrib import admin

from customer_management.models import Customer
from mailing_management.models import NewsLetter
from message_management.models import Letter
from users.models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','email','phone_number')
    search_fields = ('email','phone_number')

@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','fio','email','description')
    search_fields = ('fio','email')

@admin.register(NewsLetter)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','start_time','end_time','message')
    search_fields = ('start_time','end_time','message')

@admin.register(Letter)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','email_subject','letter_body')
    search_fields = ('email_subject',)