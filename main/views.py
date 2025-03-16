# main/views.py

import urllib.parse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseBadRequest
from .models import Cpu, Motherboard, Memory, Case, CpuCooler, InternalHardDrive, Os

# Импортируем все нужные функции из compatibility.py
from .compatibility import filter_compatible_motherboards,filter_compatible_cases,filter_compatible_memory_for_build


def index(request):
    """
    Главная страница. Здесь же кнопка для переключения режима совместимости.
    """
    # Получаем состояние из сессии, по умолчанию пусть будет True (включено)
    compatibility_on = request.session.get('compatibility_on', True)

    context = {
        'compatibility_on': compatibility_on
    }
    return render(request, 'main/index.html', context)


def toggle_compatibility(request):
    """Переключает состояние совместимости в сессии."""
    current = request.session.get('compatibility_on', True)
    request.session['compatibility_on'] = not current
    return redirect('main:index')


def list_components(request, category):
    """
    Выводит список комплектующих в зависимости от категории.
    Учитывает режим совместимости (compatibility_on) для разных категорий.
    """
    compatibility_on = request.session.get('compatibility_on', True)

    # Получаем уже выбранные компоненты из сессии
    selected_cpu_id = request.session.get('build_cpu')
    selected_motherboard_id = request.session.get('build_motherboard')
    selected_os_id = request.session.get('build_os')

    # Загружаем объекты (если есть)
    current_cpu = Cpu.objects.filter(id=selected_cpu_id).first() if selected_cpu_id else None
    current_motherboard = Motherboard.objects.filter(id=selected_motherboard_id).first() if selected_motherboard_id else None
    current_os = Os.objects.filter(id=selected_os_id).first() if selected_os_id else None

    # Сопоставляем категорию с моделью
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
        # Если включена проверка совместимости, применяем фильтры:
        if category == 'motherboard' and current_cpu:
            # Фильтруем матплаты по сокету CPU
            items = filter_compatible_motherboards(current_cpu, items)

        elif category == 'case' and current_cpu:
            # Фильтруем корпуса по мощности PSU относительно TDP CPU
            items = filter_compatible_cases(current_cpu, items)

        elif category == 'memory':
            # Фильтруем модули ОЗУ по CPU, MB, OS (если выбраны)
            items = filter_compatible_memory_for_build(items,
                                                       cpu=current_cpu,
                                                       motherboard=current_motherboard,
                                                       os_=current_os)
        # Для остальных категорий (cpu_cooler, hdd, os)
        # пока не показано, но при желании можно расширять.

    context = {
        'category': category,
        'items': items,
        'compatibility_on': compatibility_on,
    }
    return render(request, 'main/category_list.html', context)


@login_required
def add_to_build(request, category, item_id):
    """
    Добавляет выбранную комплектующую в 'сборку' пользователя (сессия).
    """
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
        model_class.objects.get(id=item_id)  # если нет, бросит исключение
    except model_class.DoesNotExist:
        return HttpResponseBadRequest("Такого объекта не существует")

    request.session[key] = item_id
    request.session.modified = True

    return redirect('main:show_build')


@login_required
def show_build(request):
    """
    Отображает текущую сборку пользователя (по данным в сессии).
    """
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
    """
    Удаляет выбранную категорию комплектующего из сборки (сессии).
    """
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
    """
    Детальный просмотр характеристик выбранного комплектующего + ссылка на DNS.
    """
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

    # Генерация ссылки на DNS
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
