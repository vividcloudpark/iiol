
from datetime import datetime, timedelta
def get_ipaddress(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_remain_sec_of_today():
    now=datetime.now()
    midnight=datetime(now.year, now.month, now.day, 23, 59, 59)
    time_remain=midnight-now
    return time_remain.total_seconds()
