
from Cryptodome.Cipher import AES
import binascii, os
from time import mktime
import re
import json
from datetime import date, datetime

def decrypt(encrypted_value, session=None, pos_func=None):
    if encrypted_value is not None:
        sec = AES
        cipher = sec.new((os.getenv('KEY')).encode("utf8"), AES.MODE_ECB)
        result = cipher.decrypt(binascii.unhexlify(
            encrypted_value)).rstrip().decode('latin-1')
        if result is not None:
            if pos_func:
                return pos_func(result)
            return result
    return encrypted_value

def encrypt(value, session=None):
    if value is not None:
        if isinstance(value, (list, dict)):
            value = dumps(value, True)
        else:
            value = str(value)
        data = value.encode('latin-1', 'ignore').decode('latin-1')
        sec = AES
        cipher = sec.new(os.getenv('KEY').encode('utf-8'), AES.MODE_ECB)
        data = (data + (" " * (16 - (len(data) % 16)))
                ).encode('latin-1', 'ignore')
        return binascii.hexlify(cipher.encrypt(data))
    return value

def serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    if isinstance(obj, date):
        return obj.strftime('%d/%m/%Y')


def serial_date(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.strftime('%d/%m/%Y')


def serial_datetime_2(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime('%Y-%m-%d 00:00:00')


def dumps(data, is_date=False):
    default = serial
    if is_date:
        default = serial_date
    return json.dumps(data, default=default)


def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, str) and re.match('^\d{4}-\d{2}-\d{2} 00:00:00$', v):
            try:
                dct[k] = datetime.strptime(v, "%Y-%m-%d 00:00:00")
            except Exception:
                pass
    return dct