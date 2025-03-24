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


# --- НОВАЯ ЛОГИКА ДЛЯ КОРПУСА (CASE) ПО ФОРМ-ФАКТОРУ --- #

def parse_form_factor(text):
    """
    Пробуем определить «ранг» форм-фактора из строки.
    Например, "Mini ITX", "Micro ATX", "ATX", "Extended ATX" и т.д.

    Возвращаем целое число (1,2,3,4 и т.п.), где больше = больше форм-фактор.
    Если распознать не удалось — возвращаем None.
    """
    if not text:
        return None

    text = text.lower()

    # В этом словаре указываем известные форм-факторы и их «ранги»
    ranks = {
        "mini itx": 1,
        "micro atx": 2,
        "atx": 3,
        "extended atx": 4,
    }

    # Проверяем, упоминается ли какой-то из ключей в строке
    for ff, rank in ranks.items():
        if ff in text:
            return rank

    return None


def is_case_compatible_with_motherboard(motherboard, case):
    """
    Сравниваем form_factor материнки и type корпуса.
    Если ранг корпуса >= ранга материнки, то совместимы.
    """
    mb_rank = parse_form_factor(motherboard.form_factor or "")
    case_rank = parse_form_factor(case.type or "")

    # Если не можем распарсить — считаем несовместимым
    if mb_rank is None or case_rank is None:
        return False

    return case_rank >= mb_rank


def filter_compatible_cases_by_motherboard(motherboard, all_cases):
    """
    Отфильтровать корпуса, у которых form_factor (rank) >= form_factor материнки.
    """
    result = []
    for c in all_cases:
        if is_case_compatible_with_motherboard(motherboard, c):
            result.append(c)
    return result


# --- Ниже всё, что касается памяти, ОС и т.д. --- #

def parse_psu_wattage(psu_text):
    """
    (Эта функция вам может больше не понадобиться, 
     если вы убираете проверки мощности БП, 
     но оставим на всякий случай)
    """
    if not psu_text:
        return None
    text = psu_text.strip().upper()
    match = re.search(r'(\d+)\s?W', text)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None


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
    if os_ is None:
        return True
    if os_.max_memory is None:
        return True

    mem_capacity = parse_memory_capacity(memory)
    if mem_capacity is None:
        return False

    return mem_capacity <= os_.max_memory


def is_memory_compatible_with_motherboard(memory, motherboard):
    if motherboard is None:
        return True
    if motherboard.max_memory is None:
        return True

    mem_capacity = parse_memory_capacity(memory)
    if mem_capacity is None:
        return False

    return mem_capacity <= motherboard.max_memory


def is_memory_compatible_with_cpu(memory, cpu):
    # Заглушка — считаем, что любой CPU поддерживает до 128 ГБ
    assumed_cpu_max = 128
    mem_capacity = parse_memory_capacity(memory)
    if mem_capacity is None:
        return False
    return mem_capacity <= assumed_cpu_max


def filter_compatible_memory_for_build(all_memory, cpu=None, motherboard=None, os_=None):
    """
    Возвращает список модулей памяти, которые удовлетворяют:
      - Проверке с CPU (если CPU указан)
      - Проверке с Motherboard (если MB указана)
      - Проверке с OS (если OS указана)
    """
    result = []
    for mem in all_memory:
        if cpu and not is_memory_compatible_with_cpu(mem, cpu):
            continue
        if motherboard and not is_memory_compatible_with_motherboard(mem, motherboard):
            continue
        if os_ and not is_memory_compatible_with_os(mem, os_):
            continue
        result.append(mem)
    return result
