from django.shortcuts import render, redirect
from .models import Student, MonthlyFee, Course, Income, Expense, Category
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.db.models import Q



# Create your views here.
def home(request):
    return render(request, 'management/index.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'management/student_list.html', {'students':students})

def fee_detail(request, id):
    student = Student.objects.get(id=id)
    monthly_fees = student.monthly_fees.order_by('-year', '-month')
    return render(request, 'management/fee_detail.html', {'student':student, 'monthly_fees':monthly_fees})

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
        Income.objects.create(source=f"Fee Payment by {student.name}", amount=amount, desc=f"Fee Payment by {student.name} - Student Id : {student.id}", date=date_paid)
        messages.success(request, 'Fees Submit Successfully')
        redirect('home')
    return render(request, 'management/add_monthly_fee.html', {'student':student})

        
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        father_name = request.POST['father_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        father_number = request.POST['father_number']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        course = request.POST.get('course')
        education = request.POST['education']
        address = request.POST['address']
        belongs_to = request.POST['belongs_to']
        admission_date = request.POST['admission_date']
        monthly_fee = request.POST['monthly_fee']
        Student.objects.create(name=name, father_name=father_name, phone_number=phone_number, email=email, 
        course=Course.objects.get(name=course), monthly_fee=monthly_fee, dob=dob, gender=gender, father_number=father_number,
        education=education, address=address, belongs_to=belongs_to, admission_date=admission_date,)
        messages.success(request, 'Student Added Successfully.')
        redirect('student_list')
    courses = Course.objects.all()
    return render(request, 'management/add_student.html', {'courses':courses})

def accounts_dashboard(request):
    total_income = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    balance =  total_income - total_expenses

    monthly_income =  Income.objects.filter(date__month=datetime.now().month).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_expenses = Expense.objects.filter(date__month=datetime.now().month).aggregate(Sum('amount'))['amount__sum'] or 0
    month = datetime.now().strftime("%B")
    return render(request, 'management/accounts.html', {
        'total_income':total_income,
        'total_expenses':total_expenses,
        'balance':balance,
        'monthly_income':monthly_income,
        'monthly_expenses':monthly_expenses,
        'month':month,
    })


def add_income(request):
    if request.method == 'POST':
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST.get('date')
        desc = request.POST['desc']
        Income.objects.create(source=source, amount=amount, date=date, desc=desc)
        messages.success(request, 'Income Added SuccessFully.')
        return redirect('accounts')
    return render(request, 'management/add_income.html')


def add_expense(request):
    if request.method == 'POST':
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']
        desc = request.POST['desc']
        Expense.objects.create(category=Category.objects.get(name=category), amount=amount, date=date, desc=desc)
        messages.success(request, 'Expense Added SuccessFully.')
        return redirect('accounts')
    categorys = Category.objects.all()
    return render(request, 'management/add_expense.html', {'categorys':categorys})

def add_expense_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, 'Added Expense Category Successfully.')
        return redirect('add_expense')
    return render(request, 'management/add_expense_category.html')

def expense_details(request):
    expenses = Expense.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        date = request.POST.get('date', '').strip()
        month = request.POST.get('month', '').strip()
        year = request.POST.get('year', '').strip()
        amount = request.POST.get('amount', '').strip()

        # filtering on the base on provided fields
        filters = Q()
        if search:
            filters &= Q(category__name__icontains = search) | Q(desc__icontains = search)
        if date:
            try:
                filters &= Q(date = datetime.strptime(date, '%Y-%m-%d').date())
            except ValueError:
                pass
        if month:
            filters &= Q(date__month = month)
        if year:
            filters &= Q(date__year = year)

        if amount:
            filters &= Q(amount__icontains = amount)
        expenses = Expense.objects.filter(filters)

    return render(request, 'management/expenses_details.html', {'expenses':expenses})


def income_details(request):
    incomes = Income.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        date = request.POST.get('date', '').strip()
        month = request.POST.get('month', '').strip()
        year = request.POST.get('year', '').strip()
        amount = request.POST.get('amount', '').strip()

        # filtering on the base on provided fields
        filters = Q()
        if search:
            filters &= Q(source__icontains = search) | Q(desc__icontains = search)
        if date:
            try:
                filters &= Q(date = datetime.strptime(date, '%Y-%m-%d').date())
            except ValueError:
                pass
        if month:
            filters &= Q(date__month = month)
        if year:
            filters &= Q(date__year = year)

        if amount:
            filters &= Q(amount__icontains = amount)
        incomes = Income.objects.filter(filters)

    return render(request, 'management/income_details.html', {'incomes':incomes})


# logic to generate Fee Slip

