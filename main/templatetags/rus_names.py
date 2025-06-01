from django import template

register = template.Library()

_RUS = {
    "cpu":          "Процессоры",
    "motherboard":  "Материнские платы",
    "memory":       "Оперативная память",
    "case":         "Корпуса",
    "cpu_cooler":   "Кулеры CPU",
    "hdd":          "Жёсткие диски",
    "os":           "Операционные системы",
    "video_card":   "Видеокарты",
    "powersupply":  "Блоки питания",
}

@register.filter(name="rus_category")
def rus_category(slug: str) -> str:
    return _RUS.get(slug, slug.title())
