from twocaptcha import TwoCaptcha
from decouple import config
import requests, time

class Solve_Captcha:

    def __init__(self):
        self._key = config('CAPTCHA')

    def resolve_recaptcha(self,url):
        print('Resolvendo captcha')
        two = TwoCaptcha(self._key)
        return two.recaptcha(self._key, url) 
    
    def resolve_normal(self,img_path):

        content = {'file': open(img_path, 'rb')}

        data = {'key': self._key, 'method': 'post'}

        r = requests.post('http://2captcha.com/in.php', files=content, data=data)

        if r.ok and r.text.find('OK') > -1:

            reqid = r.text[r.text.find('|')+1:]

        for timeout in range(40):

            r = requests.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(self._key, reqid))

            if r.text.find('CAPCHA_NOT_READY') > -1:

                print(r.text)

                time.sleep(3)

            if r.text.find('ERROR') > -1:

                return []

            if r.text.find('OK') > -1:

                return r.text.split('|')[1]
    
    def resolve_hcaptcha(self,sitekey,url):

        r = requests.post('https://2captcha.com/in.php?key={}&method=hcaptcha&sitekey={}&pageurl={}'.format(self._key,sitekey,url))

        if r.ok and r.text.find('OK') > -1:

            reqid = r.text[r.text.find('|')+1:]

        for timeout in range(40):

            r = requests.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(self._key, reqid))

            if r.text.find('CAPCHA_NOT_READY') > -1:

                print(r.text)

                time.sleep(3)

                r = requests.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(self._key, reqid))

            if r.text.find('ERROR') > -1:

                return []

            if r.text.find('OK') > -1:

                return r.text.split('|')[1]

        
    def recaptcha(self,sitekey,url):
        r = requests.post('https://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}'.format(self._key,sitekey,url))

        if r.ok and r.text.find('OK') > -1:

            reqid = r.text[r.text.find('|')+1:]

        for timeout in range(40):

            r = requests.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(self._key, reqid))

            if r.text.find('CAPCHA_NOT_READY') > -1:

                print(r.text)

                time.sleep(3)

                r = requests.get('http://2captcha.com/res.php?key={0}&action=get&id={1}'.format(self._key, reqid))

            if r.text.find('ERROR') > -1:

                return []

            if r.text.find('OK') > -1:

                return r.text.split('|')[1]
