from django.shortcuts import render,get_object_or_404
# Create your views here.
from .models import MenuItem, Category


def home(request):

    return render(request,'home.html')



def menu(request):

    return render(request,'menu.html')


def reservation(request):

    return render(request,'reservation.html')

def contact(request):

    return render(request,'contact.html')


def food(request,cid,categoryName):
    category = get_object_or_404(Category,id=cid)
    menu_items = MenuItem.objects.filter(category_items=category)
    return render(request,'food.html',{'category':category,'menu_items':menu_items})