from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_attendance/$', views.add_attendance, name='add_attendance'),
    url(r'^show_attendances/$', views.show_attendances, name='show_attendances'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    # url(r'^calendar/(?P<month_id>(\*)/$', views.month_calendar, name='month_calendar'),
    path('calendar/<month_id>/', views.month_calendar, name='month_calendar'),

]