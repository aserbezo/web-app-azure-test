from django.shortcuts import render


# Create your views here.
def get_last_location(request):
    return render(request,'mapshow/map.html')