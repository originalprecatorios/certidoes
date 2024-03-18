import requests
import os, time
from selenium.webdriver.common.by import By
from utils.selenium_classes import Selenium_classes

class Estadual:
    def __init__(self,pData,pCaptcha):
        print('Robo Estadual')
        self._data = pData
        self.timeout_seconds = 10
        self._captcha = pCaptcha        
        
    def login(self):
        if os.path.isdir('{}'.format(self._data['path'])):
            print("O diretório existe!")
        else:
            os.makedirs('{}'.format(self._data['path']))
        
        resposta = self._captcha.recaptcha('6LdoPeUUAAAAAIC5yvhe7oc9h4_qf8_Vmq0xd9GU','https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx')
        #resposta =''
        url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

        payload = {}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'Cookie': 'ASP.NET_SessionId=4crvekcr53g4yi5ilzokj4dv'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

        payload = f'__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=I7S%2FZwBOM8Z%2FK396B7sf4Ys%2BgRbgod3RHdEISM8laezRbrb5O%2FNi2GoX1BGKc5F%2F2c%2BAa8RmxNO8o4OV8IlTsS1NSWOnRaWqZkwHCzf8Uqf0Y0MSn3%2FEakovUnWv0TE%2F%2B2jgLKyfev2KC6AKa7dqEISH%2Bf0z0zN4poWIhNZvlJBh9I6%2FLSwI6B%2BjvBrWqjYb3yvmNjVTp4f4oAxrri20DBeEpPfGTnXej%2F7HS9hMvpxF37KVMhXoJ7gunKWMO791FgXa6alXp9vSnRhmefodixFsDelXlW1NkPEC1zyZqhwSX8a%2FYJcmTuqvGM7JNKs29gz1KjeJSuQtXqhFL8isVH5Bbwt9YEZ39pwZ1qIgpFc7UKone1zTIilDnKJJsY2AWrITToyX%2Bw%2BraykVCTUvaNXQ4Zkg3w1F7XDQSTZmY9ejovg9sUFPFNfqyHBpd5sS7hnDGA%3D%3D&__VIEWSTATEGENERATOR=1C0B1C53&__EVENTVALIDATION=TNe2TPGIjRebcTN0TpV3Ou7R1Bhw3%2BmpYpzfNxDtMoS75g6ezPkc%2BN4ze3Hd46P5mbmZ%2FeY85M5vKtrvV3NEaCleIkUvS%2BaWJzVLZ%2F8y%2B8GcsgujnFzu11PJh5uCz0YiBWEN0qk5omSNXg3kHb92MJ%2FnHz37w1e8TG27gt4HdbAvMArgKm2luv1BFcGG7bfew4dydg%3D%3D&ctl00%24MainContent%24grupoDocumento=cpfradio&ctl00%24MainContent%24txtDocumento={self._data["cpf"]}&ctl00%24MainContent%24btnPesquisar=%20Emitir%20&g-recaptcha-response={resposta}&ctl00%24MainContent%24hdgrecaptcha={resposta}'
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www10.fazenda.sp.gov.br',
        'Referer': 'https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'Cookie': 'ASP.NET_SessionId=4crvekcr53g4yi5ilzokj4dv'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        '''url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

        payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=R48j9Oo3CDFf%2FjqgaTvosq%2BfqHFmcGDLJ04OGzgk%2BMmJBSPBnmvilTwk8mHEMSTJM4DenQXh3M%2BhpOzZQGqvTMbrAx%2B7Xw%2BpkoEhY0agcQYv0esRs9ptlDtKQSCEyiMtHonv29dqNYZ2VskDlcTzLALvUuHoW88f34Sf8XgzWibeRp5Wo6%2FpSkdcr68hYLGFU3y4Yjo%2BEDSyrB0q9iBEJT3LqSNVAoQ5Dfq0eMZa6sKi%2FT3toQmYIodldsCw0GUJ4U80YW5Lhtg3s5PBeVgIYeSZOyky2DsnviojRvaOwTYbrEHfBABg047QZvy0VzMrPDVGMrw%2BT8rSWTPHTNUbpg5NivM9u%2F8q0cvKL4eKypiutEeCRuK9zBj7a5t0nz9CAvAsF7EQinYgjP8ZiUaWGoP%2F7jHSS9L%2Bu%2FXmCuDaR3Q2ByDaavWuspv0Bid3SOOVcywt7g%3D%3D&__VIEWSTATEGENERATOR=1C0B1C53&__EVENTVALIDATION=mcKH9PmY7J%2FN7q0lULNNbrsUBz4NpZLG2naZxTA5GqPokRnQmZWKF1IqK5484mBwrx7n2A%2BprVcmBe9rSNNE9r0yVjdoa5MrMvMdDbo7x1M2ZeDsx40O5WRUz4fq%2FcTzCYkIvD%2B1Zk01dyTTHLvKRfgaZjpE9wJOGmEtuLQvOOiwsAWP%2BAOen1viyhg%2BbblV%2B%2BmQ5g%3D%3D&ctl00%24MainContent%24grupoDocumento=cpfradio&ctl00%24MainContent%24txtDocumento={}&ctl00%24MainContent%24btnPesquisar=%2BEmitir%2B&g-recaptcha-response={}&ctl00%24MainContent%24hdgrecaptcha={}'.format(self._data['cpf'],resposta,resposta)
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www10.fazenda.sp.gov.br',
        'Referer': 'https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.request("POST", url, headers=headers, data=payload)'''
        

        url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/ImpressaoCertidaoNegativa.aspx"

        payload = {}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'Cookie': 'ASP.NET_SessionId=4crvekcr53g4yi5ilzokj4dv'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=self.timeout_seconds)
        if response.text.find('Não foi possível emitir a Certidão Negativa.') >=0:
            return 'Não foi possível emitir a Certidão Negativa.'
        try:
            response = self.download_archive()
        except:
            time.sleep(5)
            response = self.download_archive()

        if response.headers.get("content-type") == "application/pdf":
            with open(os.path.join(self._data['path'],'2- CND ESTADUAL.pdf'), "wb") as pdf_file:
                pdf_file.write(response.content)
            print("Arquivo PDF salvo com sucesso.")
        else:
            raise ValueError

        
        for arquivo in os.listdir(self._data['path']):
            if arquivo.find('2- CND ESTADUAL.pdf') > -1:
                print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                return True
        raise ValueError


    def download_archive(self):
        url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/ImpressaoCertidaoNegativa.aspx"

        payload = '__EVENTTARGET=ctl00%24MainContent%24btnImpressao&__EVENTARGUMENT=&__VIEWSTATE=ibV4TjGjew%2BKUs5f2%2BxIfUMxW%2BtLzWbQPu50DHU9GKEQXwF%2FZxPW0Lv1CeSXuE5PTD9Yi6GpHydmiU5wD%2F2Z9IS1acmH7%2B8qMTlGNPw0CsnmiVuRTvJNTfYslEK7BYnbPylEa2P%2BgjhMrfo5Ta2Ma5131pXkVPuZx9JeoC1DCGjfbM5ezkqKAHRR8TJyj%2F4TeEhw%2Bb54H4PbC%2BfAMVoTwVhAdGk9nH2AmTjx7mrzyK%2Fu2T%2BrNLGmOWeZBBIVrL%2BZLrlbfpmyhfetqeyO7qDiqWgWtDqpb%2BAuxN%2FxVxeUHkUSwcTrcxHDxr5kdUwbFO%2BfMPS0sH3VMFRftgJeKP9GM78Toi3gRzHDIfnJsOQ8GUA0kN%2BnoID8j9qApQpNOIHfekaAhklFQpVeBb2CWopq67EgU60Pl7A2GEGUJnUVNqqBWwnetHvpxF1%2BveSJxK%2Fk4piqvbqQvkRg8IZVlJN1ErEwrVA26xW%2FyPwdyTdOv0jaPs68R1Ip4MzHOSwj15MG97LwNpAEc6PvSc4Rd1mrOarrhsWiZH7NUcpFzGCW5luu3C9AuCcMv3%2BhGU5Q8e14ky4qL4AkinyoWdGrNiPP8goHJi8GDzfteMb2DFLpHZfzddBui0trXlOXfHKinwr0lP5D4FwOJ68I3VxVii%2FG%2FoQSHaP7JffLWX7ph7FbdkL3HN5h4UjxqqmzxhLGnfqTRa%2FgMcfzA6PdI9RDR6sPX1AkJq5MnP%2BB7hTXGlj4h5JVphXTQijPRBHgLHulm7Fq82600nb83Eg%2BEDImtSWhJcMtPL9%2FE7J5d9bbzXMQx3ct5HKPOg%2BMZqhZJDw4eu%2FuPui0iGjC4pb1ASUioPRj%2FypMcbRyCX0aHjCKu3y7QUg5qcS1FpgF%2BrtKra8%2Fns6EqdtU9YP9rgZg9ovQgw%2B2BjgQy1xXaprV8gJEAGOlAiv3yxrSij8Q%2FMcqZOpKpKGBMjN%2BLsfKzCxNzP2K6%2FJQhj6PGjFcVVMoxsw%2F7kZYJ1GI1DDGARWYjmJNcjNdzbiyUeAe9RxaIOuAZKr0xM%2F%2BhvF94wVUpkYv02nxJb2dQzmHPaWwF%2BlHTEcHmZFBBx0GLzX9Agy7jRtCK7T9uZeIc6Ru6OBNOvYAFeKuJ4dCrmIzMAhcXYqQb2eGH%2Fs9KKWo7L2RmE803lzRLY5H27nu8JMQ01CLTThkW%2FEdf2PmWpGWOujrD5jiz0%2FZNekVGNfdLyPNWLxT3AjGuIHiumcCMAHz8LfOLgrb2cxuFyapAUe9d4%2FFwSyk%2BptjIbSxfNDTBufYWt5tMGqV0FkM2aU2E1PkWmmoki%2BnY%2FjO%2FHK44IH1MAum8VwXI0KvQI7FbopblNoCuyhYTcsZqkoPPNIH%2FRGxOQ4xKSYn%2B2LJvgtHHlG0n8jV&__VIEWSTATEGENERATOR=FBC43117&__EVENTVALIDATION=OQQYV7NsDqViTiciGjI0g%2FihxjKTeKrO9hRMN3s%2FcGNpZifjcKsYDnBOoOnu610k1CBwpUS5gLfx0RpDao%2BA1uukfrK0ADcCKzO8GJkkFfid3%2FlnxXLil%2FlWlWW2hlkPKFZefw%3D%3D'
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www10.fazenda.sp.gov.br',
        'Referer': 'https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/ImpressaoCertidaoNegativa.aspx',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'Cookie': 'ASP.NET_SessionId=4crvekcr53g4yi5ilzokj4dv'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        return response
        
