from urllib import request
from decouple import config
import requests, time

class Captcha:

    def __init__(self,data,page,method = "userrecaptcha"):
        self.data_site_key = data
        self.page_url = page
        self.method = method
        pass

    def _saldo(self):
        u = f"https://2captcha.com/res.php?key={config('API_KEY')}&action=getbalance&json=1"
        r = requests.get(u)
        return r.json().get("request")

    def _resposta(self,id):
        u2 = f"https://2captcha.com/res.php?key={config('API_KEY')}&action=get&id={int(id)}&json=1"
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

    def _resolve(self):
        if self.method == "userrecaptcha":
            u1 = f"https://2captcha.com/in.php?key={config('API_KEY')}&method={self.method}&googlekey={self.data_site_key}&pageurl={self.page_url}&json=1&invisible=1"
        else:
            u1 = f"https://2captcha.com/in.php?key={config('API_KEY')}&method={self.method}&sitekey={self.data_site_key}&pageurl={self.page_url}&json=1"

        r1 = requests.get(u1)
        #print(r1.json())
        #print("RESOLVENDO O RECAPTCHA")
        id = r1.json().get("request")

        return self._resposta(id)

    def _resolve_img(self):
        payload = {'key': config('API_KEY'), 'method': 'base64', 'json' : 1, 'body' : self.data_site_key}
        resposta = requests.post("https://2captcha.com/in.php", data=payload)
        
        #print(resposta.json())
        id = resposta.json().get("request")

        return self._resposta(id)
        
