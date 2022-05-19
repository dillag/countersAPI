from django.db.models import TextChoices


class EventStatus(TextChoices):
    start = "1", 'Сантехник'
    ready = "2", 'Электрик'
    success = "3", 'Муж на час'
