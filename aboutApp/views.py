from django.shortcuts import render

# Create your views here.
def show_us(request):
    return render(request,'about.html')