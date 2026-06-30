"""
Reports app — date-range filtering utility.
"""
from datetime import date, timedelta
from calendar import monthrange


def apply_date_filter(queryset, date_range: str, date_from=None, date_to=None):
    """Apply a named or custom date range to a queryset with a 'date' field."""
    today = date.today()

    if date_range == 'today':
        return queryset.filter(date=today)
    elif date_range == 'yesterday':
        return queryset.filter(date=today - timedelta(days=1))
    elif date_range == 'week':
        return queryset.filter(date__gte=today - timedelta(days=7))
    elif date_range == 'month':
        return queryset.filter(date__gte=today - timedelta(days=30))
    elif date_range == 'current_month':
        return queryset.filter(date__year=today.year, date__month=today.month)
    elif date_range == 'prev_month':
        first_day = today.replace(day=1) - timedelta(days=1)
        return queryset.filter(date__year=first_day.year, date__month=first_day.month)
    elif date_range == 'custom':
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        return queryset
    return queryset
