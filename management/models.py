from django.db import models
from datetime import datetime

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id} - {self.name}"
    

class MonthlyFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='monthly_fees')
    month = models.CharField(max_length=20, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'), ('September', 'September'),
        ('October', 'October'), ('November', 'November'), ('December', 'December')])
    year = models.IntegerField(default=datetime.now().year)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.month}-{self.year}"


class Income(models.Model):
    source = models.CharField(max_length=100, help_text="Source of income e.g Students Fee")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.now)
    desc = models.TextField(blank=True, help_text="Additional Deatils about the income source")

    def __str__(self):
        return f"{self.source} - {self.amount}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, help_text="Category e.g Salaries, Investment, Digital Expenses")

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.now)
    desc = models.TextField(blank=True, help_text="Details About the Expenses")

    def __str__(self):
        return f"{self.category} - {self.amount}"
    

