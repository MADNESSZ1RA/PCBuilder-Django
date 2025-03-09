# compatibility.py

def is_compatible_cpu_motherboard(cpu, motherboard):
    """
    Простейшая проверка совместимости CPU и Motherboard по сокету.
    Возвращает True/False.
    """
    return cpu.socket == motherboard.socket


def filter_compatible_motherboards(cpu, all_motherboards):
    """
    Возвращает список матер. плат из all_motherboards,
    которые совместимы с данным cpu.
    """
    compatible = []
    for mb in all_motherboards:
        if is_compatible_cpu_motherboard(cpu, mb):
            compatible.append(mb)
    return compatible
