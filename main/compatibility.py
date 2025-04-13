import re


def is_compatible_cpu_motherboard(cpu, motherboard):
    return cpu.socket == motherboard.socket


def filter_compatible_motherboards(cpu, all_motherboards):
    compatible = []
    for mb in all_motherboards:
        if is_compatible_cpu_motherboard(cpu, mb):
            compatible.append(mb)
    return compatible


def parse_form_factor(text):
    if not text:
        return None
    text = text.lower()
    ranks = {
        "mini itx": 1,
        "micro atx": 2,
        "atx": 3,
        "extended atx": 4,
    }

    for ff, rank in ranks.items():
        if ff in text:
            return rank

    return None


def is_case_compatible_with_motherboard(motherboard, case):
    mb_rank = parse_form_factor(motherboard.form_factor or "")
    case_rank = parse_form_factor(case.type or "")

    if mb_rank is None or case_rank is None:
        return False

    return case_rank >= mb_rank


def filter_compatible_cases_by_motherboard(motherboard, all_cases):
    result = []
    for c in all_cases:
        if is_case_compatible_with_motherboard(motherboard, c):
            result.append(c)
    return result


def parse_psu_wattage(psu_text):
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
    modules_text = memory.modules
    if not modules_text:
        return None

    modules_text = modules_text.lower().replace(' ', '')

    match = re.match(r'(\d+)x(\d+)gb', modules_text)
    if match:
        try:
            count = int(match.group(1))
            size_gb = int(match.group(2))
            return count * size_gb
        except ValueError:
            return None

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
    assumed_cpu_max = 128
    mem_capacity = parse_memory_capacity(memory)
    if mem_capacity is None:
        return False
    return mem_capacity <= assumed_cpu_max


def filter_compatible_memory_for_build(all_memory, cpu=None, motherboard=None, os_=None):
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
