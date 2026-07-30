from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
def home(request):
    # return HttpResponse("<h1>Welcome to Home<h2>")
    return render(request,'APP2/home.html')

def about(request):
    # return HttpResponse("<h1>welcome to about<h2>")
    return render(request,'APP2/about.html')

