import requests
import os, time
from selenium.webdriver.common.by import By
from utils.selenium_classes import Selenium_classes

class Estadual:
    def __init__(self,pData,pCaptcha):
        print('Robo Estadual')
        self._data = pData
        self._captcha = pCaptcha        
        
    def login(self):
        if os.path.isdir('{}'.format(self._data['path'])):
            print("O diretório existe!")
        else:
            os.makedirs('{}'.format(self._data['path']))
        
        resposta = self._captcha.recaptcha('6LdoPeUUAAAAAIC5yvhe7oc9h4_qf8_Vmq0xd9GU','https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx')
        #resposta =''
        url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

        payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=R48j9Oo3CDFf%2FjqgaTvosq%2BfqHFmcGDLJ04OGzgk%2BMmJBSPBnmvilTwk8mHEMSTJM4DenQXh3M%2BhpOzZQGqvTMbrAx%2B7Xw%2BpkoEhY0agcQYv0esRs9ptlDtKQSCEyiMtHonv29dqNYZ2VskDlcTzLALvUuHoW88f34Sf8XgzWibeRp5Wo6%2FpSkdcr68hYLGFU3y4Yjo%2BEDSyrB0q9iBEJT3LqSNVAoQ5Dfq0eMZa6sKi%2FT3toQmYIodldsCw0GUJ4U80YW5Lhtg3s5PBeVgIYeSZOyky2DsnviojRvaOwTYbrEHfBABg047QZvy0VzMrPDVGMrw%2BT8rSWTPHTNUbpg5NivM9u%2F8q0cvKL4eKypiutEeCRuK9zBj7a5t0nz9CAvAsF7EQinYgjP8ZiUaWGoP%2F7jHSS9L%2Bu%2FXmCuDaR3Q2ByDaavWuspv0Bid3SOOVcywt7g%3D%3D&__VIEWSTATEGENERATOR=1C0B1C53&__EVENTVALIDATION=mcKH9PmY7J%2FN7q0lULNNbrsUBz4NpZLG2naZxTA5GqPokRnQmZWKF1IqK5484mBwrx7n2A%2BprVcmBe9rSNNE9r0yVjdoa5MrMvMdDbo7x1M2ZeDsx40O5WRUz4fq%2FcTzCYkIvD%2B1Zk01dyTTHLvKRfgaZjpE9wJOGmEtuLQvOOiwsAWP%2BAOen1viyhg%2BbblV%2B%2BmQ5g%3D%3D&ctl00%24MainContent%24grupoDocumento=cpfradio&ctl00%24MainContent%24txtDocumento={}&ctl00%24MainContent%24btnPesquisar=%2BEmitir%2B&g-recaptcha-response={}&ctl00%24MainContent%24hdgrecaptcha={}'.format(self._data['cpf'],resposta,resposta)
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASP.NET_SessionId=zydipx5n45rvzshk2urlj1ug',
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

        response = requests.request("POST", url, headers=headers, data=payload)
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

        payload='__EVENTTARGET=ctl00%24MainContent%24btnImpressao&__EVENTARGUMENT=&__VIEWSTATE=L2ojZFnla5Hk523CiNkRCKZ%2BAJ4%2BPhBeG715Yaremh2alxkCSXPnjdtJ6I%2BC%2FSwW%2FYf3lHKgBoN1vn5%2BZMDUFWy2VWrtchPI2Itp5TbnJChBcg3vvW%2F5L8jOIbjc8zY8R%2Fuga8nmJ%2F81Kr2KtMitmbWG%2F%2FKNG7zlxPQaPzb1xoGpU5D%2BUry%2F%2BzYmxbCgav2zaIjRgf22GKvsnM%2BSWNXwxCh4JMwQ8bYZ1KMS1W0%2BVOkojmuc8TZ2L6ig5iFZHtysVLoFiWG8M9IV%2FZqgg1rjCvi%2FqTaHFPAj8SJLCKyhfV7dgGbKLDRZp8fA7Pd4oV3HKkvSQqObdxULLY49mbfMHmTYOZGGDjMmO5IklK8ebSSDU1pMPny%2FHqHqz%2BdeWerGD5P1kn27hwADisg21HkZQZtaCnT30bGK9%2BOlRiQTpzV%2BdKedTvO0b9qKCFN19yoh4jg%2BNIxoUkZIYeLRnoR6dHlwC86XBQeJ1tc%2FBZzYp4gqdYESqAaFsjXJ9y%2FYRjcxy%2BPjs%2F9hv3Uodhv2WrwGAVfhTwI8pFN3b1pCE4AprkPucFthy1Oprocqsy60DilnZJCvCOmKCDRaiNyDgxbI%2FrSL9qSG2psYQNTIoSMpzYQuC3OUi3fEyBm75%2FKvah6EPinoDO0uHuhGLsg%2BRvC%2FSoMYUKldd7tIrpvS2Ah%2BZSgns9i6zjswXHjUUF25lLWL9ROES08jAqcJony5%2BaTe6zSphBx%2BADhAiKNYi0Vq0fSeOhKWLb6JqdD63%2Bg4w1DI604%2BJzMslXi%2B21uQf9lF%2FO1fCzBkAY5TI6ScTUZSziVa6Yg2%2BuPaDByHnv3d7E28I2aqeCtD7Rf08sc4I8CbWcwgw70be%2FMxgeT7uK62FLDjccc1pWxRYAQyAYXtphUM3vI7uKdAE2buqglGIQHhkvKuK5Wwcm4JMAAPpQ2y3TNusuIkON3s62LbyyATprvzfPh1S92GTYoncQWFy6aoxfdT2aYjrKoYuKlTrubucoiBNJ9meklc8s%2BYEuQhVfq4csAQPmcTICaeQ00ha6YI35ALODVOunRGrpUlUEzPm3zR2hKrBENUpwe4bVoHD%2FldouIs38PwQcBSzw6hJOKxcXW8WAqdj6RBSXsV6ejePQ5DWV6DDWgZMTOlSXJgyF13mUORAOlTiRXuHUb8yvw8gc%2FtHhWXvLS%2ByYXaDlnrl4sZ2%2FO00nzJckRSiVNj0jKTuKISx8X%2FqdD7UR7%2B6XPV6l0VQZA7vSbcvW5rshN%2BoE%2FoRn68QA5U0SpkmedvvWmmX9h9KjR%2FX5LdEZ3fIpSOVY2HdWUxiOn5JkGFkTDtOU8atirP%2FeMatJsjCBmL%2BHLLTp74w1Rox%2FNAyjHnHpaajddh3nvHpihbH49FDFbuzQFF%2BCvx&__VIEWSTATEGENERATOR=FBC43117&__EVENTVALIDATION=iqfgrqkLjqw%2BBKl5Ox%2Fjxo5koICJlg8yYKZOvKkk63HrPtHAW6eyG3oFv22Dy5GY6dGWaB1eUkVMvrlysYNV8vYoinHCsawjrzzA2caecL5ycQ7RdU15dkFGNOCCX6bjJE9%2FZQ%3D%3D'
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASP.NET_SessionId=zydipx5n45rvzshk2urlj1ug; ASP.NET_SessionId=u01lehxza4yutytaxwpr4ajk',
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
        'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response
        
