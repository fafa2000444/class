from django.shortcuts import render
from django.http import HttpResponse
from .models import Market, Mobile, Monitor, Laptop

def home(request):
    return HttpResponse('welcome to the market')




def marketv(request):
    markets = Market.objects.all()
    mobiles = Mobile.objects.all()
    monitors = Monitor.objects.all()
    laptops = Laptop.objects.all()
    
    return render(request, 'jahadf/market.html', {
        'markets': markets,
        'mobiles': mobiles,
        'monitors': monitors,
        'laptops': laptops,
    })

# Create your views here.
