from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
import datetime


class Date(models.Model):
    My_Date = models.DateField(unique=True)

    @property
    def getting_day(self):
        return str(self.My_Date.day)

    def __str__(self):
        return str(self.My_Date)

    def get_attendances(self):
        all_atts = self.attendance_set.all().order_by('User_id')
        all_atts_string = ''
        for att in all_atts:
            all_atts_string += f'{att.User.Name}:{att.Value} | '
        return all_atts_string

    def all_presence(self):
        all_full_days = self.attendance_set.filter(Value=1.0).count()
        all_half_days = self.attendance_set.filter(Value=0.5).count()
        all_absents = self.attendance_set.filter(Value=0.0).count()

        return f'Full Days : {all_full_days} | Half Days : {all_half_days} | Abesnts : {all_absents}'



class Employee(models.Model):
    Name = models.CharField(max_length=200)
    CF_LB = models.FloatField(verbose_name='Carry Forward Leave Balance', default=0)
    Leave_Balance = models.FloatField(default=0)


    def __str__(self):
        return self.Name



VALUE_CHOICES = ((1.0, 'Full Day'), (0.5, 'Half_Day'), (0.0, 'Absent'))


class Attendance(models.Model):
    # AtDate = models.DateField(auto_now_add=False, verbose_name='Date', null=True, blank=True)
    Date = models.ForeignKey(Date, on_delete=models.CASCADE, null=True, blank=True)
    User = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Value = models.FloatField(choices=VALUE_CHOICES)

    def __str__(self):
        return "{0} | {1} | {2}".format(self.Date.My_Date, self.User, self.Value)

def date_save(sender, instance, **kwargs):
    if not instance.Date:
        today_date = Date.objects.get_or_create(My_Date=datetime.date.today())[0]
        instance.Date = today_date
        instance.save()

post_save.connect(date_save, sender=Attendance)

def lb_auto_call(sender, instance, **kwargs):
    instance.User.save()
post_save.connect(lb_auto_call, sender=Attendance)
#
def lb_save(sender, instance, **kwargs):
    all_atts = instance.attendance_set.all()
    # instance.nk()
    total_count = all_atts.count()
    atts_count = sum([i.Value for i in all_atts])
    if not instance.Leave_Balance == (instance.CF_LB + atts_count - total_count):
        instance.Leave_Balance = (instance.CF_LB + atts_count - total_count)
        instance.save()


pre_save.connect(lb_save, sender=Employee)