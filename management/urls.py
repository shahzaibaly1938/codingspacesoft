from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:id>/', views.student_detail, name='student_detail'),
    path('students/fee/<int:id>/', views.fee_detail, name='fee_detail'),
    path('students/<int:student_id>/add-fee/', views.add_monthly_fee, name='add_monthly_fee'),
    path('students/add-student/', views.add_student, name='add_student'),
    path('accounts/', views.accounts_dashboard, name='accounts'),
    path('accounts/add-income/', views.add_income, name='add_income'),
    path('accounts/add-expense/', views.add_expense, name='add_expense'),
    path('accounts/add-expense/category', views.add_expense_category, name='add_expense_category'),
    path('accounts/expenses-details', views.expense_details, name='expenses_details'),
    path('accounts/income_details', views.income_details, name='income_details'),
    path('dues/', views.due_fees, name='due_fees'),
    path('certificate/<int:student_id>/', views.certificate, name='certificate'),
    path('final-certificate/', views.final_certificate, name='final_certificate'),

]