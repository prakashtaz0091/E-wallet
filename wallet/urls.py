from django.urls import path, re_path
from . import views

app_name = 'wallet'


urlpatterns = [
    path('',views.home, name="home"),
    path('transfer-fund/',views.transferFund, name="transfer-fund"),
    path('error-page/',views.error, name="error-page"),
    path('success-page/',views.successPage, name="success-page"),
]