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
    
    def _resolve_img(self,data_site_key):
        
        payload = {'key': self._key, 'method': 'base64', 'json' : 1, 'body' : data_site_key}
        resposta = requests.post("https://2captcha.com/in.php", data=payload)
        
        #print(resposta.json())
        id = resposta.json().get("request")

        return self._resposta(id)
    
    def _resposta(self,id):
        u2 = f"https://2captcha.com/res.php?key={self._key}&action=get&id={int(id)}&json=1"
        time.sleep(5)
        i = 1
        while True:
            r2 = requests.get(u2)
            print(f"\033[33m\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[{i}] Tentativas\033[0;0m ", end="", flush=True)

            if r2.json().get("status") == 1:
                form_tokon = r2.json().get("request")
                print(f"\033[32m\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[{i}] Resolvido\033[0;0m ", end="", flush=True)
                break
            i += 1
            time.sleep(5)
        return form_tokon
