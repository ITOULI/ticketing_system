from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ticket_all, name='store_home'),
    path('<slug:slug>', views.ticket_detail, name='ticket_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]
