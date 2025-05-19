from django.urls import path
from .views import home,marketv

urlpatterns= [
    path ('home/',home),
    path ('overview/',marketv),
]
