from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import login, logout_then_login



urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_attendance/$', views.add_attendance, name='add_attendance'),
    url(r'^show_attendances/$', views.show_attendances, name='show_attendances'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    # url(r'^calendar/(?P<month_id>(\*)/$', views.month_calendar, name='month_calendar'),
    path('calendar/<month_id>/', views.month_calendar, name='month_calendar'),

    url(r'^login/$', login, {'template_name': 'portal/portal_login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),

]