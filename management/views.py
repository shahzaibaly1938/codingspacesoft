from django.shortcuts import render, redirect
from .models import Student, MonthlyFee, Course
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'management/index.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'management/student_list.html', {'students':students})

def student_detail(request, id):
    student = Student.objects.get(id=id)
    monthly_fees = student.monthly_fees.order_by('-year', '-month')
    return render(request, 'management/student_detail.html', {'student':student, 'monthly_fees':monthly_fees})

def add_monthly_fee(request, student_id):
    student = Student.objects.get(id = student_id)
    if request.method == 'POST':
        month = request.POST['month']
        year = request.POST['year']
        amount = request.POST['amount']
        is_paid = request.POST.get('is_paid')
        if is_paid == 'on':
            is_paid = True
        elif is_paid == 'off':
            is_paid = False
        date_paid = request.POST.get('date_paid')
        MonthlyFee.objects.create(student=student, month=month, year=year, amount=amount, is_paid=is_paid, date_paid=date_paid)
        messages.success(request, 'Fees Submit Successfully')
        redirect('home')
    return render(request, 'management/add_monthly_fee.html', {'student':student})

        
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        father_name = request.POST['father_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        course = request.POST.get('course')
        monthly_fee = request.POST['monthly_fee']
        Student.objects.create(name=name, father_name=father_name, phone_number=phone_number, email=email, course=Course.objects.get(name=course), monthly_fee=monthly_fee)
        messages.success(request, 'Student Added Successfully.')
        redirect('student_list')
    courses = Course.objects.all()
    return render(request, 'management/add_student.html', {'courses':courses})