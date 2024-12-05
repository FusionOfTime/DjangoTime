from django.shortcuts import render
from datetime import datetime

# Create your views here.

def index_page(request):
    context = {
        "name": "Арсений"
    }
    return render(request, "index.html", context)
def time_page(request):
    current_time = datetime.now()
    formatted_date = current_time.strftime("%d.%m.%Y")
    formatted_time = current_time.strftime("%H:%M:%S")
    context = {
        "current_date": formatted_date,
        "current_time": formatted_time
    }
    return render(request, "time.html", context)