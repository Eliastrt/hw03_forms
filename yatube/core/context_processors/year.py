import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    today = datetime.datetime.now()
    year = today.year - 23
    return {
        'year': year,
    }