from django.shortcuts import render

# Create your views here.
def InternHome(request):
    return render(request, 'users/intern_home.html')