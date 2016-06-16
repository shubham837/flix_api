import pytz

Time_FORMAT = {
    'day': '%d %b %y',
    'meridian_time': '%I:%M %p',
}

DEFAULT_CURRENCY = 'EURO'

TIMEZONE = pytz.timezone('Asia/Kolkata')

REDIS_AUTH_KEY_FORMAT = "gr_auth_key:%s"
REDIS_ACCESS_TOKEN_KEY_FORMAT = "gr_acc_tok:%s"
