import ast
from urllib.parse import unquote

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
import random

from first.forms import StringInputForm
from first.models import StringRequest, StudentStats

history = []

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


def expression_page(request):
    num_terms = random.randint(2, 4)
    expression = ""
    result = 0
    ops = ["+", "-"]
    for i in range(num_terms):
        num = random.randint(10, 99)
        if i == 0:
            result += num
            expression += str(num)
        else:
            op = random.choice(ops)
            if op == "+":
                result += num
            else:
                result -= num
            expression += f" {op} {num}"

    history.append({
        'expression': expression,
        'result': result
    })

    context = {
        'expression': expression,
        'result': result,
    }
    return render(request, "expression.html", context)


def history_page(request):
    context = {
        'history': history,
    }
    return render(request, "history.html", context)
# Часть 1: Удаление последнего выражения
def delete_last_expression(request):
    if history:
        history.pop()
    return render(request, "delete.html")


# Часть 2: Очистка истории
def clear_history(request):
    history.clear()
    return render(request, "clear.html")



# Часть 3: Добавление нового выражения
def new_expression(request):
    expr_param = request.GET.get('expr')

    if expr_param is not None:
        try:
            expr_param = unquote(expr_param)
            result = eval(expr_param)
            history.append({'expression': expr_param, 'result': result})
            return render(request, 'new_expression.html', {'message': "Ваше выражение добавлено"})
        except Exception:
            return render(request, 'new_expression.html', {'message': "Некорректный формат выражения"})
    else:
        return render(request, "new_expression.html", {
            "message": "Для добавления выражения используйте URL с параметром ?expr=выражение"
        })
def analyze_string(input_str):
    words = []
    numbers = []
    current_word = ""
    current_number = ""
    for char in input_str:
        if char.isalnum():
            if char.isdigit():
                current_number += char
            else:
                 if current_number:
                     numbers.append(current_number)
                     current_number = ""
                 current_word += char
        elif char.isspace():
            if current_word:
                words.append(current_word)
                current_word = ""
            if current_number:
                numbers.append(current_number)
                current_number = ""
    if current_word:
        words.append(current_word)
    if current_number:
        numbers.append(current_number)
    return words, numbers


@login_required
def str2words_page(request):
    if request.method == 'POST':
        form = StringInputForm(request.POST)
        if form.is_valid():
            input_str = form.cleaned_data['input_string']
            words, numbers = analyze_string(input_str)
            word_count = len(words)
            char_count = len(input_str)
            current_time = datetime.now()
            StringRequest.objects.create(
                user=request.user,
                request_date=current_time.date(),
                request_time=current_time.time(),
                input_string=input_str,
                word_count=word_count,
                char_count=char_count,
            )
            context = {
                'words': words,
                'numbers': numbers,
                'word_count': word_count,
                'char_count': char_count,
                'form': form,
            }
            return render(request, "str2words.html", context)
    else:
        form = StringInputForm()
    return render(request, "str2words.html", {'form': form})


@login_required
def str_history_page(request):
    history = StringRequest.objects.filter(user=request.user).order_by('-request_date','-request_time')
    return render(request, 'str_history.html', {'history': history})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def clicker_page(request):
    try:
       student_stats = StudentStats.objects.get(user=request.user)
    except StudentStats.DoesNotExist:
       student_stats = StudentStats.objects.create(user=request.user)
    context = {
       'student_stats': student_stats,
    }
    return render(request, 'clicker.html', context)

@login_required
def save_stats(request):
    if request.method == "POST":
        try:
            hp = int(request.POST.get('hp'))
            iq = int(request.POST.get('iq'))
            happiness = int(request.POST.get('happiness'))
            student_stats = StudentStats.objects.get(user=request.user)
            student_stats.hp = hp
            student_stats.iq = iq
            student_stats.happiness = happiness
            student_stats.save()
            return JsonResponse({'status': 'ok'})
        except Exception:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

