
from Cryptodome.Cipher import AES
import binascii, os

def decrypt(encrypted_value, session=None, pos_func=None):
    if encrypted_value is not None:
        sec = AES
        cipher = sec.new((os.environ['KEY']).encode("utf8"), AES.MODE_ECB)
        result = cipher.decrypt(binascii.unhexlify(
            encrypted_value)).rstrip().decode('latin-1')
        if result is not None:
            if pos_func:
                return pos_func(result)
            return result
    return encrypted_value
