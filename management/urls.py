from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:id>/', views.student_detail, name='student_detail'),
    path('students/<int:student_id>/add-fee/', views.add_monthly_fee, name='add_monthly_fee'),
    path('students/add-student/', views.add_student, name='add_student'),

]