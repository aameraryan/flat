from django.shortcuts import render, get_list_or_404
from .models import *
from django.http import HttpResponse, HttpResponseRedirect



def home(request):
    return render(request, 'portal/home.html')


def add_attendance(request):
    if request.method=='POST':
        att_date = Date.objects.create(My_Date=request.POST['date'])
        for input_name in request.POST:
            if '--' in input_name:
                emp = Employee.objects.get(id=str(input_name.split('--')[-1]))
                emp_value = float(request.POST[input_name])
                Attendance.objects.create(Date=att_date, User=emp, Value=emp_value)
        return render(request, 'portal/home.html', {'messages': ('Successfully added Attendance of {date}'.format(date=att_date.My_Date),)})
    else:
        return render(request, 'portal/add_attendance.html', {'employees': Employee.objects.all()})


def show_attendances(request):
    employees = Employee.objects.all()
    dates = Date.objects.all().order_by('My_Date')
    return render(request, 'portal/show_attendances.html', {'employees': employees, 'dates': dates})

def calendar(request):
    all_months = {date.My_Date.strftime("%B-%Y") for date in Date.objects.all().distinct()}
    return render(request, 'portal/calendar.html', {'all_months': all_months})


def month_calendar(request, month_id):
    months_list_numbers = ['...', 'January', 'February', 'March', 'April', 'May','June',
                           'July', 'August', 'September', 'October', 'November', 'December']
    my_month = int(months_list_numbers.index(month_id.split('-')[0]))
    my_year = int(month_id.split('-')[1])
    dates = Date.objects.filter(My_Date__month=my_month, My_Date__year=my_year).order_by('My_Date')
    employees = Employee.objects.all()
    return render(request, 'portal/show_attendances.html', {'employees': employees,
                                                            'dates': dates, 'month': month_id})


