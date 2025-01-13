from django import template
from datetime import datetime, timedelta
from django.utils import timezone
register = template.Library()

@register.filter
def humanize_date(value):
    if not value:
        return ""

    # Получаем текущее время с учетом часового пояса
    now = timezone.now()

    # Если объект value не имеет часового пояса (naive), приводим его к aware
    if value.tzinfo is None:
        value = timezone.make_aware(value)

    # Вычисляем разницу между текущим временем и временем создания
    delta = now - value

    # Логика для вывода разницы в человекочитаемом виде
    if delta < timedelta(minutes=1):
        return "Только что"
    elif delta < timedelta(hours=1):
        minutes = delta.seconds // 60
        return f"{minutes} минут назад" if minutes > 1 else "1 минуту назад"
    elif delta < timedelta(days=1):
        hours = delta.seconds // 3600
        return f"{hours} часов назад" if hours > 1 else "1 час назад"
    elif value.date() == now.date():
        return "Сегодня"
    elif value.date() == (now - timedelta(days=1)).date():
        return "Вчера"
    else:
        return value.strftime("%d.%m.%Y")