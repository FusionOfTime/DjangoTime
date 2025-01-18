import ast
from urllib.parse import unquote

from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import random

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


