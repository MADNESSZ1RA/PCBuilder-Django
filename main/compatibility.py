# compatibility.py

import re

def is_compatible_cpu_motherboard(cpu, motherboard):
    """
    Простейшая проверка совместимости CPU и Motherboard по сокету.
    Возвращает True/False.
    """
    return cpu.socket == motherboard.socket


def filter_compatible_motherboards(cpu, all_motherboards):
    """
    Возвращает список матер. плат из all_motherboards,
    которые совместимы с данным cpu (по сокету).
    """
    compatible = []
    for mb in all_motherboards:
        if is_compatible_cpu_motherboard(cpu, mb):
            compatible.append(mb)
    return compatible


def parse_psu_wattage(psu_text):
    """
    Пытаемся извлечь из строки блока питания (case.psu) число ватт.
    Пример: "500W" или "500 W" -> 500
    Если не удаётся, возвращаем None.
    """
    if not psu_text:
        return None

    text = psu_text.strip().upper()
    # Ищем шаблон вида "<число>W" или "<число> W"
    match = re.search(r'(\d+)\s?W', text)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None


def is_psu_sufficient_for_cpu(cpu, case):
    """
    Проверяем, хватает ли мощности БП (case.psu) для CPU.tdp.
    Упрощённая логика: если psu >= cpu.tdp * 1.3, то считаем достаточно.
    """
    wattage = parse_psu_wattage(case.psu)
    if wattage is None:
        # Если не смогли распарсить PSU, считаем несовместимым
        return False
    return wattage >= cpu.tdp * 1.3


def parse_memory_capacity(memory):
    """
    Пробуем вычислить общий объём памяти (ГБ) из поля memory.modules.
    Примеры:
      "2 x 8GB" -> 16
      "1 x 16GB" -> 16
      "8GB" -> 8
    Возвращаем целое число (ГБ) или None, если не смогли распарсить.
    """
    modules_text = memory.modules
    if not modules_text:
        return None

    modules_text = modules_text.lower().replace(' ', '')

    # Шаблон "N x MGB"
    match = re.match(r'(\d+)x(\d+)gb', modules_text)
    if match:
        try:
            count = int(match.group(1))
            size_gb = int(match.group(2))
            return count * size_gb
        except ValueError:
            return None

    # Шаблон "MGB"
    match2 = re.match(r'(\d+)gb', modules_text)
    if match2:
        try:
            return int(match2.group(1))
        except ValueError:
            return None

    return None


def is_memory_compatible_with_os(memory, os_):
    """
    Проверяем, вписывается ли объём памяти в max_memory ОС.
    os_.max_memory — целое число (или None).
    memory.modules — строка, парсим её.
    """
    if os_ is None:
        # Если ОС не выбрана, не проверяем
        return True

    if os_.max_memory is None:
        # Если в БД нет ограничения, считаем совместимым
        return True

    mem_capacity = parse_memory_capacity(memory)
    if mem_capacity is None:
        # Не удалось определить объём, считаем несовместимым
        return False

    return mem_capacity <= os_.max_memory


def is_memory_compatible_with_motherboard(memory, motherboard):
    """
    Проверяем, вписывается ли объём памяти в max_memory матер. платы.
    """
    if motherboard is None:
        return True

    if motherboard.max_memory is None:
        return True

    mem_capacity = parse_memory_capacity(memory)
    if mem_capacity is None:
        return False

    return mem_capacity <= motherboard.max_memory


def is_memory_compatible_with_cpu(memory, cpu):
    """
    Проверка максимальной оперативной памяти, которую «может обработать» CPU.
    У CPU нет поля max_memory, так что сделаем заглушку (128 ГБ).
    """
    # Например, считаем, что любой CPU поддерживает до 128 ГБ
    assumed_cpu_max = 128
    mem_capacity = parse_memory_capacity(memory)
    if mem_capacity is None:
        return False

    return mem_capacity <= assumed_cpu_max


def filter_compatible_cases(cpu, all_cases):
    """
    Отфильтровать корпуса, у которых psu хватает для CPU.
    """
    result = []
    for case in all_cases:
        if is_psu_sufficient_for_cpu(cpu, case):
            result.append(case)
    return result


def filter_compatible_memory_for_build(all_memory, cpu=None, motherboard=None, os_=None):
    """
    Возвращает список модулей памяти, которые удовлетворяют:
      - Проверке с CPU (если CPU указан)
      - Проверке с Motherboard (если MB указана)
      - Проверке с OS (если OS указана)
    """
    result = []
    for mem in all_memory:
        # CPU совместимость
        if cpu and not is_memory_compatible_with_cpu(mem, cpu):
            continue
        # Motherboard совместимость
        if motherboard and not is_memory_compatible_with_motherboard(mem, motherboard):
            continue
        # OS совместимость
        if os_ and not is_memory_compatible_with_os(mem, os_):
            continue
        result.append(mem)
    return result
