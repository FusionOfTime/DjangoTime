from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

# Create your views here.

def index_page(request):
    context = {
        "name": "Арсений",
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
def calc_page(request):
    try:
        a = int(request.GET.get('first_number', 0))
        b = int(request.GET.get('second_number', 0))
        answer = a + b
        context = {
            'first_number': a,
            'second_number': b,
            'answer_number': answer,
        }
        return render(request, 'calc.html', context)
    except ValueError:
        return HttpResponse("Некорректные входные данные.  Передайте целые числа для 'a' и 'b'.")

