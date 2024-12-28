from django.contrib import admin
from . models import Student, Course, MonthlyFee, Income, Expense, Category
# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(MonthlyFee)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Category)