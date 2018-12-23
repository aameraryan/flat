from django.shortcuts import render, get_list_or_404, reverse
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.contrib import messages



def home(request):
    if request.user.is_authenticated:
        if Month_Leaves.objects.count() != 0:
            try:
                last_added = Month_Leaves.objects.first().Last_Added.month
            except:
                last_added = 'not added yet'
            this_month = datetime.date.today().month
            if last_added != this_month:
                context = {'show_add_leave': 1}
            else:
                context = {'show_add_leave': 2}
        else:
            context = {'show_add_leave': 1}
        return render(request, 'portal/home.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def emp_refresh(request):
    for employee in Employee.objects.all():
        employee.save()
    messages.success(request, "Successfully Refreshed the protal on {0}".format(datetime.date.today()))
    return HttpResponseRedirect(reverse('home'))
    # return render(request, 'portal/home.html', {'messages':('Successfully Refreshed the protal on {0}'.format(datetime.date.today()),)})


@login_required
def add_attendance(request):
    if request.method=='POST':
        att_date = Date.objects.create(My_Date=request.POST['date'])
        for input_name in request.POST:
            if '--' in input_name:
                emp = Employee.objects.get(id=str(input_name.split('--')[-1]))
                emp_value = float(request.POST[input_name])
                Attendance.objects.create(Date=att_date, User=emp, Value=emp_value)
        messages.success(request, 'Successfully added Attendance of {date}'.format(date=att_date.My_Date))
        return HttpResponseRedirect(reverse('home'))
        # return render(request, 'portal/home.html', {'messages': ('Successfully added Attendance of {date}'.format(date=att_date.My_Date),)})
    else:
        json_dates = json.dumps([str(date.My_Date) for date in Date.objects.all()])
        return render(request, 'portal/add_attendance.html', {'employees': Employee.objects.all(), 'json_dates': json_dates})


@login_required
def calendar(request):
    all_months = {date.My_Date.strftime("%B-%Y") for date in Date.objects.all().distinct()}
    return render(request, 'portal/calendar.html', {'all_months': all_months})

@login_required
def month_calendar(request, month_id):
    months_list_numbers = ['...', 'January', 'February', 'March', 'April', 'May','June',
                           'July', 'August', 'September', 'October', 'November', 'December']
    my_month = int(months_list_numbers.index(month_id.split('-')[0]))
    my_year = int(month_id.split('-')[1])
    dates = Date.objects.filter(My_Date__month=my_month, My_Date__year=my_year).order_by('My_Date')
    employees = Employee.objects.all()
    return render(request, 'portal/month_attendances.html', {'employees': employees,
                                                            'dates': dates, 'month': month_id})


@login_required
def add_month_leaves(request):
    try:
        last_added = Month_Leaves.objects.first().Last_Added.month
    except:
        Month_Leaves.objects.create()
        last_added = 'no month added'
    this_month = datetime.date.today().month
    if last_added != this_month:
        count = 0
        for employee in Employee.objects.all():
            if employee.DOJ < datetime.date.today()-datetime.timedelta(days=90):
                employee.CF_LB += 1.5
                employee.save()
                count+=1
        last_month_leave = Month_Leaves.objects.first()
        last_month_leave.Last_Added = datetime.date.today()
        last_month_leave.Added_Times += 1
        last_month_leave.save()
        messages.success(request, 'Successfully added month leaves to {0} employees.'.format(count))
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.success(request, 'Already added for this month')
        return HttpResponseRedirect(reverse('home'))