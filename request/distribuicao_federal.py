import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.firefox.options import Options
from PIL import Image
import img2pdf
import requests
import time
import shutil
from bson.objectid import ObjectId
from create_certificate.send_email import Email_enviar

class Distribuicao_federal():
    def __init__(self,pData,pMongo,pCaptcha,pInstancia,pNome_documento,pTipo):
        self._data = pData
        self._bdMongo = pMongo
        self._captcha = pCaptcha
        self._instancia = pInstancia
        self._nome = pNome_documento
        self._tipo = pTipo
        self._template = os.path.join(os.getcwd(),'templates/response_css.text')
        self._pasta = self._data['path']
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')
        self._save = '/opt/certidao/download/distribuicao_federal{}'.format(self._data['cpf'])
        try:
            if os.path.isdir(f'{self._save}') is False:
                os.makedirs(f'{self._save}')
            else:
                shutil.rmtree(self._save)
                os.makedirs(f'{self._save}')
        except:
            pass
        
        if self._instancia == '1':
            self._tribunal = 'SJSP'
                
        else:
            self._tribunal = 'TRF'
        self._key = 0

    def initial(self):
        url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao"

        payload={}
        headers = {
        'authority': 'web.trf3.jus.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8M4U1UgBugxMsTHCu75vosyDFcBgdfuxueHrndVgW1T2vx32YdbH90lKJprNN7j56m9kwLJ3_T7yxa4SLWvcOVPaM3Ww0B14HIEI0aXVyertDXOJup82ghB5HKW-ViRLYVE7RYILbqBQKscEkLB4Z0o; __utmz=138416428.1658941714.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.2106690254.1658941714; __utma=138416428.2106690254.1658941714.1658941714.1665690419.2; ak_bmsc=634DC6D59E0314C741A7F374A35A8378~000000000000000000000000000000~YAAQmNMnF3v/tx+HAQAApmp/OBMxBPS7KxAbT8nB+SkQ5wwHGRj4PV955vNJylAyhp+NK/lizdX+zGgboInJtfSw5Z/3k+u96BP0GWPSu9XV8rqh6Kxz3XpqC+6lwca4XNMc3674o2dj5YlB7OKApCaX9y+m2KP5JNRLFbdhFLZL7NPSKa88b2kxP8K1MibnrX6PZ1bwfac36vQN0d2F2ePLefwRUKdPSwdIN/x1KTzUuufAqfmLoko/Qgf9sVZchrkmNYz/aS5x5XQ7btWsEBwhcEMEsM/Ze839p+DPg9+s2gL8G+4z/16xAPakpOTuyEybqddKNk3TcZ8FvSEtSVqRF7T9TcmQmvOLKfeF11iXg4ju1ffYbDzCtT8YmGSRmWEyAgHVZAjaYnuwsvsOiYdahBNmnLpR5uvL5XLQyAA2dDmbJ4C7jG3wPlORZsQ7+Kl4PPtsXZu8Nr4+D6LVee9Tn/swPDylRL4e1mjcUGZGErq3RljcCvaZ; bm_sv=AE0AC61403AE8ACF6F16627744D21F64~YAAQGoY0F5aIvRGHAQAAvgqhOBNYhBkWaDhWTVwXPKCBhXcn4F8m+iUSy+Bpvg9vHN53pXn4UW503/zZNJjDofOF7drt8UOIg5gzP56lkBp1ON/6OtjurNGrLbjHKSZa42FOPaDVwkaWZLMloBYukngFc/WMy5Gu+LJ2rkVbHOFR6VYIQoxs0BqW2gc79bWI3/wuepNYHbEUXEEWCZksjonfipSgtIrPM8pMu7kZq3efpCJq5Jj+XPB0ni48nvBNPJw=~1; bm_sv=AE0AC61403AE8ACF6F16627744D21F64~YAAQhgopFzQLQTOHAQAAdfuhOBMo7wc7UgR0GOFuEQQw4g+OHxdusyLa94LMj5Q/rDVdbMiukVonHYOHMjTiKk8ANUFhdJO1wjZOTQJJM9UrrBFIuNhu4EiXaqGhUNTq/NKUJIJwaawGyYBW4FJUYiyEDzz6MX9IHyoNqFR7vw7a9SgohfTQ0mgIxTyBTKs7SiWxobmPWabGSMMI8+WSKtDjzaWDMHGrxrlqr4PQNxLWQQERIpGoxQpsNjKAxMJsgSI=~1',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #bm = str(response.cookies).split('bm_sv=')[1].split(' for')[0]
        self._token = response.text.split('__RequestVerificationToken')[1].split('/>')[0].split('value=')[1].replace('"','').strip()
        self._response = self._captcha.recaptcha('6Le_CtAZAAAAAEbTeETvetg4zQ7kJI0NH5HNHf1X','https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao')
        #response = ''

    def creat_html(self):
        url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Gerar"

        payload='Tipo={}&TipoDeDocumento=CPF&Documento={}&Nome={}&NomeSocial=&Abrangencia={}&g-recaptcha-response={}&__RequestVerificationToken={}'.format(self._tipo,self._data['cpf'],self._data['nome'],self._tribunal,self._response,self._token)
        headers = {
        'authority': 'web.trf3.jus.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8M4U1UgBugxMsTHCu75vosyDFcBgdfuxueHrndVgW1T2vx32YdbH90lKJprNN7j56m9kwLJ3_T7yxa4SLWvcOVPaM3Ww0B14HIEI0aXVyertDXOJup82ghB5HKW-ViRLYVE7RYILbqBQKscEkLB4Z0o; __utmz=138416428.1658941714.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.2106690254.1658941714; __utma=138416428.2106690254.1658941714.1658941714.1665690419.2; ak_bmsc=634DC6D59E0314C741A7F374A35A8378~000000000000000000000000000000~YAAQmNMnF3v/tx+HAQAApmp/OBMxBPS7KxAbT8nB+SkQ5wwHGRj4PV955vNJylAyhp+NK/lizdX+zGgboInJtfSw5Z/3k+u96BP0GWPSu9XV8rqh6Kxz3XpqC+6lwca4XNMc3674o2dj5YlB7OKApCaX9y+m2KP5JNRLFbdhFLZL7NPSKa88b2kxP8K1MibnrX6PZ1bwfac36vQN0d2F2ePLefwRUKdPSwdIN/x1KTzUuufAqfmLoko/Qgf9sVZchrkmNYz/aS5x5XQ7btWsEBwhcEMEsM/Ze839p+DPg9+s2gL8G+4z/16xAPakpOTuyEybqddKNk3TcZ8FvSEtSVqRF7T9TcmQmvOLKfeF11iXg4ju1ffYbDzCtT8YmGSRmWEyAgHVZAjaYnuwsvsOiYdahBNmnLpR5uvL5XLQyAA2dDmbJ4C7jG3wPlORZsQ7+Kl4PPtsXZu8Nr4+D6LVee9Tn/swPDylRL4e1mjcUGZGErq3RljcCvaZ; bm_sv=AE0AC61403AE8ACF6F16627744D21F64~YAAQmNMnF/b/tx+HAQAAKrx/OBP0a8L9N0hurJJqtRp+F6FYWcgqvsEbdNPNnBxB54bNrSyUoLN22VsWTmElopOMSpyaeb66UkNT59ou7rL7MhyoLFWLL46HAARWPprhvhGnHCbXSJ+xZLLw47TnG7UP2X8omCqqOkBprHhIazhF67AxrFX63UEj9TGfEYB14DpSg5YLk9E75w0pEpNZdFf81rMLOvQfpeOerNrfMQzv3HTrRF8cMsiY+F5K/xzB1A==~1;',
        'origin': 'https://web.trf3.jus.br',
        'referer': 'https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            soup.find(id="NomeMae")
            id_certidao = soup.find(id="IdCertidao").get('value')
            token = soup.find(id="Token").get('value')
            cod_verificacao = soup.find(id="CodigoVerificacao").get('value')
            tipo_pessoa = soup.find(id="TipoPessoa").get('value')
            request_verification = response.text.split('__RequestVerificationToken')[1].split('/>')[0].split('value=')[1].replace('"','').strip()
            arquivo_espera = True
        except:
            arquivo_espera = False
            pass

        if arquivo_espera is True:
            response = self.new_data(id_certidao,token,cod_verificacao,tipo_pessoa,request_verification)
        
        if self._key == 0:
            texto_formatado = response.text.replace('<img src="/certidao-regional/imagens/trf3logo2.png" />','<img src="https://web.trf3.jus.br/certidao-regional/imagens/trf3logo2.png" />').replace('<img src="/certidao-regional/imagens/trf3brasao.png" />','<img src="https://web.trf3.jus.br/certidao-regional/imagens/trf3brasao.png" />').replace('<main role="main" class="pb-3">\r\n\r\n\r\n<div class="container">\r\n\r\n        <a class="btn btn-primary float-left" href="/certidao-regional">Página inicial</a>\r\n\r\n    <div class="row">    \r\n        <div class="col-md-4 offset-md-8 float-right">\r\n                <button id="botaoImprimirCertidao" class="btn btn-primary float-left">\r\n                    Imprimir certidão\r\n                </button>\r\n        </div>\r\n    </div>\r\n</div>\r\n\r\n','')
        else:
            return False
        with open(self._template) as arquivo:
            dado = arquivo.read()
        with open(self._save+'/arquivo.html', 'w') as f:
            f.write(texto_formatado)
            f.write(f'<style>{dado}</style>')
        return True
    
    def creat_document(self):
        options = Options()
        #fp = webdriver.FirefoxProfile()
        options.add_argument("--headless")
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        driver = webdriver.Firefox(options=options)
        driver.get('file:///{}'.format(self._save+'/arquivo.html'))
        time.sleep(2)
        driver.get_full_page_screenshot_as_file(self._data['path']+'{}.png'.format(self._nome))
        img_path = self._data['path']+'{}.png'.format(self._nome)
        self.convert(img_path)
        time.sleep(3)
        driver.close()
        os.remove(self._save+'/arquivo.html')
        time.sleep(2)
        for arquivo in os.listdir(self._pasta):
            if arquivo.find(self._nome+'.pdf') > -1:
                print('Download concluido para o cpf {}'.format(self._data['cpf']))
                return
        print('arquivo não foi gerado')
        driver.close()
        driver.find_element(By.ID,'submit').click()

    def convert(self,img_path):
        # storing pdf path
        pdf_path = img_path.replace('png','pdf')

        # opening image
        image = Image.open(img_path)

        # converting into chunks using img2pdf
        pdf_bytes = img2pdf.convert(image.filename)

        # opening or creating pdf file
        file = open(pdf_path, "wb")

        # writing pdf files with chunks
        file.write(pdf_bytes)

        # closing image file
        image.close()

        # closing pdf file
        file.close()

        os.remove(img_path)
        # output
        print("Successfully made pdf file")
    
    def new_data(self,id_certidao,token,cod_verificacao,tipo_pessoa,request_verification):
        url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/CadastrarPedido"

        payload='IdCertidao={}&Token={}&CodigoVerificacao={}&TipoPessoa={}&NomeMae={}&DataNascimento={}&TipoDocumento=RG&DocumentoComplementar={}&__RequestVerificationToken={}'.format(id_certidao,token,cod_verificacao,tipo_pessoa,self._data['mae'],self._data['nascimento'][8:]+"/"+self._data['nascimento'][5:7]+"/"+self._data['nascimento'][:4],self._data['rg'],request_verification)
        headers = {
        'authority': 'web.trf3.jus.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8M4U1UgBugxMsTHCu75vosyDFcBgdfuxueHrndVgW1T2vx32YdbH90lKJprNN7j56m9kwLJ3_T7yxa4SLWvcOVPaM3Ww0B14HIEI0aXVyertDXOJup82ghB5HKW-ViRLYVE7RYILbqBQKscEkLB4Z0o; __utmz=138416428.1658941714.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.2106690254.1658941714; __utma=138416428.2106690254.1658941714.1658941714.1665690419.2; ak_bmsc=634DC6D59E0314C741A7F374A35A8378~000000000000000000000000000000~YAAQmNMnF3v/tx+HAQAApmp/OBMxBPS7KxAbT8nB+SkQ5wwHGRj4PV955vNJylAyhp+NK/lizdX+zGgboInJtfSw5Z/3k+u96BP0GWPSu9XV8rqh6Kxz3XpqC+6lwca4XNMc3674o2dj5YlB7OKApCaX9y+m2KP5JNRLFbdhFLZL7NPSKa88b2kxP8K1MibnrX6PZ1bwfac36vQN0d2F2ePLefwRUKdPSwdIN/x1KTzUuufAqfmLoko/Qgf9sVZchrkmNYz/aS5x5XQ7btWsEBwhcEMEsM/Ze839p+DPg9+s2gL8G+4z/16xAPakpOTuyEybqddKNk3TcZ8FvSEtSVqRF7T9TcmQmvOLKfeF11iXg4ju1ffYbDzCtT8YmGSRmWEyAgHVZAjaYnuwsvsOiYdahBNmnLpR5uvL5XLQyAA2dDmbJ4C7jG3wPlORZsQ7+Kl4PPtsXZu8Nr4+D6LVee9Tn/swPDylRL4e1mjcUGZGErq3RljcCvaZ; bm_sv=AE0AC61403AE8ACF6F16627744D21F64~YAAQGoY0F5aIvRGHAQAAvgqhOBNYhBkWaDhWTVwXPKCBhXcn4F8m+iUSy+Bpvg9vHN53pXn4UW503/zZNJjDofOF7drt8UOIg5gzP56lkBp1ON/6OtjurNGrLbjHKSZa42FOPaDVwkaWZLMloBYukngFc/WMy5Gu+LJ2rkVbHOFR6VYIQoxs0BqW2gc79bWI3/wuepNYHbEUXEEWCZksjonfipSgtIrPM8pMu7kZq3efpCJq5Jj+XPB0ni48nvBNPJw=~1; bm_sv=AE0AC61403AE8ACF6F16627744D21F64~YAAQhgopFzQLQTOHAQAAdfuhOBMo7wc7UgR0GOFuEQQw4g+OHxdusyLa94LMj5Q/rDVdbMiukVonHYOHMjTiKk8ANUFhdJO1wjZOTQJJM9UrrBFIuNhu4EiXaqGhUNTq/NKUJIJwaawGyYBW4FJUYiyEDzz6MX9IHyoNqFR7vw7a9SgohfTQ0mgIxTyBTKs7SiWxobmPWabGSMMI8+WSKtDjzaWDMHGrxrlqr4PQNxLWQQERIpGoxQpsNjKAxMJsgSI=~1; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8M4U1UgBugxMsTHCu75vosxwWs538st7SLO3V_3QtSo7BCL6FjZnRFOmGEj6JoCbQJqxsTHUOVCcHz0-e1GECojGXVmjj6xGvmem5etYavq5_k6wpUFAlwG5CtzVtu_CzlhCVi3zzqt0zdulRHBEURK9_QkgmSvQkAj7rIFOWDgMPKD4vLicAkdp8m2jJMtQvBGu5NTY6WUnl19kpdS4LcVF7lS0XdA93Lpql4FnH_Ya',
        'origin': 'https://web.trf3.jus.br',
        'referer': 'https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Gerar',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        protocolo = response.text.split('Protocolo:</b> ')[1].split('<br')[0].strip()

        self._bdMongo._upsert({'$set': {'protocolo': protocolo}}, {"_id": ObjectId(self._data['_id'])})
        self._key = 1
        print('sistema informou o aguardo de até 5 dias para emitir certidão')
    
    def imprimir(self):
        url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Imprimir"

        payload={}
        headers = {
        'authority': 'web.trf3.jus.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8M4U1UgBugxMsTHCu75vosy3BvOJrP27NN77iGL0b_aqUgeKcjCF2rHrN71bgiQFpNe_4sjPAvtZPXWUN0cP3Txvw5tuT6Bl5Y-hXlewo6FlBcRIwi-XK6iNiGUPlFKBBiYDrXxG62Jc_sjNM7LcEbk; __utmz=138416428.1658941714.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.2106690254.1658941714; __utma=138416428.2106690254.1658941714.1658941714.1665690419.2; bm_mi=B8DB54D49507A745EBA17579F50EA55B~YAAQJEDHF82UthGHAQAAUpI+UhN2/EUd2iMDomLrEE1K1C3CjLUcw3vRS8SENV5mVVy1KxliZi5d1pvvMVKFWRoe0+5LoC6W5dcKNpIEKM7Wf3xzSAz5mbaq5Nzl93aAfOoLlMpgKUgmGTi4fCemcDtjZ1cK/tHzx5mQ13TEmpFQmaPkZ50/EbYWo7MydolFrTPB/Vkq4HgRmizlzyBIdr/4U5oAuh1uI8zNro0+pDrUTJadtdXlFZygk/+fxLCBSg4kol3TRab5LpE+KOuZREv4AklMqhKwQjcJDbguGdERqickIxzhYVkODpO493fWVQQpDSXwmZT4eL+TfqvpOKk=~1; ak_bmsc=FF6BAE79C1C9761FEAAD3845DE76D9A8~000000000000000000000000000000~YAAQJEDHF9yUthGHAQAAX8M+UhPc/A9CHjBpG4/+SLxBmemrcVbL61o81i7kbgMu1IwfLNOYFdbPEYPDUz4jpjn9PTujg6M3Cp0vokrWcDTEmdXWC4Qla2N652YRpwtXxHcTmBOj1Q8ThObDz/IPcv6caaqCNV1+gYZgyxSIYnY6FnbHufKqvqu0hwGNtyQ7vopVc2tEHaj32nYgn4irzO4D4hd12WmNunFyzHQMuf6J66z0PQwj/OLHJHeE3TYwJgA0/7VH3X4C6D2ysEYS4HrspKinIy8u79ekREK9HNA3iCZZnKV8jv4tA9xpEu/u3yFY2aD0LNWcTY4wfMtLcH+zemsZBlYAiRE/B7PaGOS26kSEVg0gydP9vze/NWCD4b35+PDyKatoPGc3GmSnn5SFN0i5njeXjAlTmaIPr0Aa9dW8vtfrAzjLC3wbxcR0t4+fPsDQL692t7XB8ADJfBeQpZqOWwfi; bm_sv=A2CF0092839FDECDC050573ADF5D05D5~YAAQJEDHF9+UthGHAQAAN8Q+UhOvFrPyXcoYWu/WCxAcR7ARFN3FJ42QNzehXZG6d8V/321PQK1vE2G+bg+EJHTVPoa63LYraDMKAUm4M1Je5RMuX+AKe6W/I6WlX8rLbAXVvH0lK4Qff9lFr+XPsNYrBzmTJaVql5FUTehRllm32aTyN0au+TGspCtqNhDOAA9sU1leO2iFiP0gQkhAVUtqvnhDq5pFAiUztYkLZ7BFop/ksEJ8zq0AYF1ZP0Trwg==~1; bm_sv=A2CF0092839FDECDC050573ADF5D05D5~YAAQdxY2F5QD7AqHAQAA2PhCUhNgadGMO9wPBpjAmJYeDVYR9g3YVi3mJ8ZGsjZIUWarp9abYeICc3+03D6UKj/dwBhybH1icc52yzwbsYOlADntw0EDkCXSySweFjNVRxR7z0xH0aGrOIzpVcPxg7Az9wmHIqH75wP3TvxolEvpXFenrpitB6DEX7p7nPkGGTxVqPFr9rOAG26pi1Bv95uJJqKiV3Ye3yfXO4LdPJPI5NllbiV8GZtrS4PzQ8hZOjo=~1',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        self._token = response.text.split('__RequestVerificationToken')[1].split('/>')[0].split('value=')[1].replace('"','').strip()
        self._response = self._captcha.recaptcha('6Le_CtAZAAAAAEbTeETvetg4zQ7kJI0NH5HNHf1X','https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Imprimir')

        url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Imprimir"

        payload='NumeroCertidao={}%2F{}&TipoDeDocumento=CPF&Documento={}&g-recaptcha-response={}&__RequestVerificationToken={}'.format(self._data['protocolo'].split('/')[0],self._data['protocolo'].split('/')[1],self._data['cpf'],self._response,self._token)
        headers = {
        'authority': 'web.trf3.jus.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8M4U1UgBugxMsTHCu75vosy3BvOJrP27NN77iGL0b_aqUgeKcjCF2rHrN71bgiQFpNe_4sjPAvtZPXWUN0cP3Txvw5tuT6Bl5Y-hXlewo6FlBcRIwi-XK6iNiGUPlFKBBiYDrXxG62Jc_sjNM7LcEbk; __utmz=138416428.1658941714.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.2106690254.1658941714; __utma=138416428.2106690254.1658941714.1658941714.1665690419.2; bm_mi=B8DB54D49507A745EBA17579F50EA55B~YAAQJEDHF82UthGHAQAAUpI+UhN2/EUd2iMDomLrEE1K1C3CjLUcw3vRS8SENV5mVVy1KxliZi5d1pvvMVKFWRoe0+5LoC6W5dcKNpIEKM7Wf3xzSAz5mbaq5Nzl93aAfOoLlMpgKUgmGTi4fCemcDtjZ1cK/tHzx5mQ13TEmpFQmaPkZ50/EbYWo7MydolFrTPB/Vkq4HgRmizlzyBIdr/4U5oAuh1uI8zNro0+pDrUTJadtdXlFZygk/+fxLCBSg4kol3TRab5LpE+KOuZREv4AklMqhKwQjcJDbguGdERqickIxzhYVkODpO493fWVQQpDSXwmZT4eL+TfqvpOKk=~1; ak_bmsc=FF6BAE79C1C9761FEAAD3845DE76D9A8~000000000000000000000000000000~YAAQJEDHF9yUthGHAQAAX8M+UhPc/A9CHjBpG4/+SLxBmemrcVbL61o81i7kbgMu1IwfLNOYFdbPEYPDUz4jpjn9PTujg6M3Cp0vokrWcDTEmdXWC4Qla2N652YRpwtXxHcTmBOj1Q8ThObDz/IPcv6caaqCNV1+gYZgyxSIYnY6FnbHufKqvqu0hwGNtyQ7vopVc2tEHaj32nYgn4irzO4D4hd12WmNunFyzHQMuf6J66z0PQwj/OLHJHeE3TYwJgA0/7VH3X4C6D2ysEYS4HrspKinIy8u79ekREK9HNA3iCZZnKV8jv4tA9xpEu/u3yFY2aD0LNWcTY4wfMtLcH+zemsZBlYAiRE/B7PaGOS26kSEVg0gydP9vze/NWCD4b35+PDyKatoPGc3GmSnn5SFN0i5njeXjAlTmaIPr0Aa9dW8vtfrAzjLC3wbxcR0t4+fPsDQL692t7XB8ADJfBeQpZqOWwfi; bm_sv=A2CF0092839FDECDC050573ADF5D05D5~YAAQkcgQAnPWuBOHAQAAH7JEUhPJtIlfjJ1yhC9+lZfMWoJPur+22w02cu34Mcicg21k+rqj6Q7FoBMsx0QYLns3f13R2ciimiDofbepXyV9iQL8tbEBoRUpok6qlFWb9zwAhvijY7w8HBxmINaPj7UX941VNdFons3+MmPlfsX5u5URhNKdDAAktCj9QxDpLq3JXCHKSsFlWCUEhPbVzF4o49/wk02u9wfa8QzCYaIslnnVYl17qEjA5pKdSNq5fbQ=~1; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8M4U1UgBugxMsTHCu75vosx2VElLmdzAhOyadv5BqQXQu9ZdCN5jbXYC5g_2rjbC5NUR6IlmJVys7QFLvekpbj3oSm_0H9-wlKY1zarDRx4Wgz89vffJb7Q6W9toj243prg5jNjWbWAemRsonrdQiXi6-hIWaQvR09M0Bi_je3H9gmWHj5HO3THbXawOXURiAkPDl3zKbrvFrsB1rqdeILuiioV87eYdMHrkPkNp4BTxi8EH4lJZC6nCHQVITNxFa4qcbLxfMKrgUKJezzXgPu6y7Ja35lv6wWl9X1fmy22-NYW4BOHpYJJ_DQjd4X3ZfTcJjNz_AK4g7bOuW1oMKuHhG8LXAnyHRqqHtNkCUsQM1WYBsK9xZN5PLNmZAkT3JA; bm_sv=A2CF0092839FDECDC050573ADF5D05D5~YAAQdxY2F5QD7AqHAQAA2PhCUhNgadGMO9wPBpjAmJYeDVYR9g3YVi3mJ8ZGsjZIUWarp9abYeICc3+03D6UKj/dwBhybH1icc52yzwbsYOlADntw0EDkCXSySweFjNVRxR7z0xH0aGrOIzpVcPxg7Az9wmHIqH75wP3TvxolEvpXFenrpitB6DEX7p7nPkGGTxVqPFr9rOAG26pi1Bv95uJJqKiV3Ye3yfXO4LdPJPI5NllbiV8GZtrS4PzQ8hZOjo=~1',
        'origin': 'https://web.trf3.jus.br',
        'referer': 'https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Imprimir',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.text.find('PODER JUDICIÁRIO') > -1:
   
            texto_formatado = response.text.replace('<img src="/certidao-regional/imagens/trf3logo2.png" />','<img src="https://web.trf3.jus.br/certidao-regional/imagens/trf3logo2.png" />').replace('<img src="/certidao-regional/imagens/trf3brasao.png" />','<img src="https://web.trf3.jus.br/certidao-regional/imagens/trf3brasao.png" />').replace('<main role="main" class="pb-3">\r\n\r\n\r\n<div class="container">\r\n\r\n        <a class="btn btn-primary float-left" href="/certidao-regional">Página inicial</a>\r\n\r\n    <div class="row">    \r\n        <div class="col-md-4 offset-md-8 float-right">\r\n                <button id="botaoImprimirCertidao" class="btn btn-primary float-left">\r\n                    Imprimir certidão\r\n                </button>\r\n        </div>\r\n    </div>\r\n</div>\r\n\r\n','')
       
            with open(self._template) as arquivo:
                dado = arquivo.read()
            with open(self._save+'/arquivo.html', 'w') as f:
                f.write(texto_formatado)
                f.write(f'<style>{dado}</style>')
            return True

        else:
            return False
    
    def email(self,ext):
        file_name = self._pasta+self._nome+'.pdf'
        smtp_config = {'host': os.getenv('SMTP_SERVE'), 'port': os.getenv('SMTP_PORT'), 'user': os.getenv('SMTP_USER'), 'passwd':os.getenv('SMTP_PASS')}
        e = Email_enviar(os.getenv('SMTP_USER'),'@#$WSDEqasw1!',file_name,[self._data['email']],smtp_config)
        texto = """Segue certificado {} para o cliente {}""".format(ext,self._data['nome'])
        e.send_email_ruralservice(self._pasta,texto,self._nome+'.pdf')

        self._bdMongo._upsert({'$unset': {'protocolo': ''}}, {"_id": ObjectId(self._data['_id'])})
