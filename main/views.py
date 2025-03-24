# main/views.py

import urllib.parse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Cpu, Motherboard, Memory, Case, CpuCooler, InternalHardDrive, Os
from .compatibility import (
    filter_compatible_motherboards,
    filter_compatible_cases_by_motherboard  # <-- новая функция
    # (можно также импортировать другие, если нужно)
)

def index(request):
    compatibility_on = request.session.get('compatibility_on', True)
    return render(request, 'main/index.html', {'compatibility_on': compatibility_on})

def toggle_compatibility(request):
    current = request.session.get('compatibility_on', True)
    request.session['compatibility_on'] = not current
    return redirect('main:index')

def list_components(request, category):
    compatibility_on = request.session.get('compatibility_on', True)

    selected_cpu_id = request.session.get('build_cpu')
    selected_motherboard_id = request.session.get('build_motherboard')
    selected_os_id = request.session.get('build_os')

    current_cpu = Cpu.objects.filter(id=selected_cpu_id).first() if selected_cpu_id else None
    current_motherboard = Motherboard.objects.filter(id=selected_motherboard_id).first() if selected_motherboard_id else None
    current_os = Os.objects.filter(id=selected_os_id).first() if selected_os_id else None

    model_map = {
        'cpu': Cpu,
        'motherboard': Motherboard,
        'memory': Memory,
        'case': Case,
        'cpu_cooler': CpuCooler,
        'hdd': InternalHardDrive,
        'os': Os,
    }
    model_class = model_map.get(category)
    if not model_class:
        return HttpResponseBadRequest("Некорректная категория")

    items = model_class.objects.all()

    if compatibility_on:
        # CPU -> фильтр motherboards
        if category == 'motherboard' and current_cpu:
            items = filter_compatible_motherboards(current_cpu, items)

        # CASE -> фильтр по форм-фактору материнки
        elif category == 'case' and current_motherboard:
            items = filter_compatible_cases_by_motherboard(current_motherboard, items)

        # memory -> при желании можно тоже дополнять (пример см. в compatibility.py)
        # os, cpu_cooler, hdd -> по желанию, если у вас есть логика

    context = {
        'category': category,
        'items': items,
        'compatibility_on': compatibility_on,
    }
    return render(request, 'main/category_list.html', context)

@login_required
def add_to_build(request, category, item_id):
    build_map = {
        'cpu': 'build_cpu',
        'motherboard': 'build_motherboard',
        'memory': 'build_memory',
        'case': 'build_case',
        'cpu_cooler': 'build_cpu_cooler',
        'hdd': 'build_hdd',
        'os': 'build_os',
    }
    key = build_map.get(category)
    if not key:
        return HttpResponseBadRequest("Некорректная категория")

    model_map = {
        'cpu': Cpu,
        'motherboard': Motherboard,
        'memory': Memory,
        'case': Case,
        'cpu_cooler': CpuCooler,
        'hdd': InternalHardDrive,
        'os': Os,
    }
    model_class = model_map.get(category)
    try:
        model_class.objects.get(id=item_id)
    except model_class.DoesNotExist:
        return HttpResponseBadRequest("Такого объекта не существует")

    request.session[key] = item_id
    request.session.modified = True
    return redirect('main:show_build')

@login_required
def show_build(request):
    build_cpu_id = request.session.get('build_cpu')
    build_motherboard_id = request.session.get('build_motherboard')
    build_memory_id = request.session.get('build_memory')
    build_case_id = request.session.get('build_case')
    build_cpu_cooler_id = request.session.get('build_cpu_cooler')
    build_hdd_id = request.session.get('build_hdd')
    build_os_id = request.session.get('build_os')

    selected_cpu = Cpu.objects.filter(id=build_cpu_id).first() if build_cpu_id else None
    selected_motherboard = Motherboard.objects.filter(id=build_motherboard_id).first() if build_motherboard_id else None
    selected_memory = Memory.objects.filter(id=build_memory_id).first() if build_memory_id else None
    selected_case = Case.objects.filter(id=build_case_id).first() if build_case_id else None
    selected_cpu_cooler = CpuCooler.objects.filter(id=build_cpu_cooler_id).first() if build_cpu_cooler_id else None
    selected_hdd = InternalHardDrive.objects.filter(id=build_hdd_id).first() if build_hdd_id else None
    selected_os = Os.objects.filter(id=build_os_id).first() if build_os_id else None

    context = {
        'cpu': selected_cpu,
        'motherboard': selected_motherboard,
        'memory': selected_memory,
        'case': selected_case,
        'cpu_cooler': selected_cpu_cooler,
        'hdd': selected_hdd,
        'os': selected_os,
    }
    return render(request, 'main/build.html', context)

def remove_from_build(request, category):
    build_map = {
        'cpu': 'build_cpu',
        'motherboard': 'build_motherboard',
        'memory': 'build_memory',
        'case': 'build_case',
        'cpu_cooler': 'build_cpu_cooler',
        'hdd': 'build_hdd',
        'os': 'build_os',
    }
    key = build_map.get(category)
    if not key:
        return HttpResponseBadRequest("Некорректная категория")

    if key in request.session:
        del request.session[key]
        request.session.modified = True
    return redirect('main:show_build')

def component_detail(request, category, item_id):
    model_map = {
        'cpu': Cpu,
        'motherboard': Motherboard,
        'memory': Memory,
        'case': Case,
        'cpu_cooler': CpuCooler,
        'hdd': InternalHardDrive,
        'os': Os,
    }
    model_class = model_map.get(category)
    if not model_class:
        return HttpResponseBadRequest("Некорректная категория")

    obj = model_class.objects.filter(id=item_id).first()
    if not obj:
        return HttpResponseBadRequest("Объект не найден")

    base_url = "https://www.dns-shop.ru/search/"
    product_name = obj.name.strip() if obj.name else ""
    search_query = urllib.parse.quote(product_name)
    dns_link = f"{base_url}?q={search_query}"

    context = {
        'obj': obj,
        'category': category,
        'dns_link': dns_link,
    }
    return render(request, 'main/detail.html', context)
