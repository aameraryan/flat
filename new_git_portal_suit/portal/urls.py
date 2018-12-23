from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import login, logout_then_login



urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_attendance/$', views.add_attendance, name='add_attendance'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    path('calendar/<month_id>/', views.month_calendar, name='month_calendar'),
    url(r'^emp_refresh/$', views.emp_refresh, name='emp_refresh'),
    url(r'^add_month_leaves/$', views.add_month_leaves, name="add_month_leaves"),
    url(r'^login/$', login, {'template_name': 'portal/portal_login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),

]