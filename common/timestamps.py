import datetime as dt

def now_utc():
    return dt.datetime.utcnow()

def iso(dt_obj):
    if not dt_obj:
        return None
    return dt_obj.isoformat()