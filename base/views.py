from django.shortcuts import render,get_object_or_404,redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages

from django.http import JsonResponse

# Create your views here.
from .models import MenuItem, Category


def home(request):

    return render(request,'home.html')


def about(request):

    return render(request,'about.html')




def menu(request):

    return render(request,'menu.html')


def reservation(request):

    return render(request,'reservation.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('your-name', '')
        email = request.POST.get('your-email', '')
        tel = request.POST.get('tel-646', '')
        subject = request.POST.get('Subject', 'No Subject')
        msg = request.POST.get('textarea-806', '')

        message = f"Name: {name}\nEmail: {email}\nPhone: {tel}\n\nMessage:\n{msg}"

        try:
            send_mail(
                subject,
                message,
                'pricetrackerprod@gmail.com',  # Sender email
                ['hellopizzaalberta@gmail.com'],  # Recipient email
                fail_silently=False,
            )
            return JsonResponse({"status": "success", "message": "Your message has been sent successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error sending email: {e}"})

    return render(request, 'contact.html')
def food(request,cid,categoryName):
    category = get_object_or_404(Category,id=cid)
    menu_items = MenuItem.objects.filter(category_items=category)
    return render(request,'food.html',{'category':category,'menu_items':menu_items})