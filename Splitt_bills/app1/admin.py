from django.contrib import admin
from .models import User, Expense, Balance

# Register your models here.

admin.site.register(User)
admin.site.register(Expense)
admin.site.register(Balance)
