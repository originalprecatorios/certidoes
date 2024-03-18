import requests
import os
from weasyprint import HTML
from utils.selenium_classes import Selenium_classes
import img2pdf
from PIL import Image

class Esaj():
    def __init__(self,pData,pCaptcha,pSelect,pNome):
        print('Esaj')
        self._data = pData
        self.timeout_seconds = 10
        self._captcha = pCaptcha
        self._select = pSelect
        self._archive = pNome
        if os.path.isdir('{}'.format(self._data['path'])):
            print("O diretório existe!")
        else:
            os.makedirs('{}'.format(self._data['path']))
        self.navegation = Selenium_classes(self._data['path'])

    def get_download(self):
        url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

        payload={}
        headers = {
        'authority': 'pje1g.trf3.jus.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'PJESID=; PJECSID=; MO=P; JSESSIONID=oZr3ml9dr61KD_zJTkaS0DP4CiJf_ZnyY7PE_54I.svlpje1g10; _ga=GA1.1.581667930.1691522903; _ga_J77T54V192=GS1.1.1691522903.1.0.1691522935.0.0.0; PJECSID=a5f71de4d2bf5fa5; PJESID=e814daa583f455f6; OAuth_Token_Request_State=9ed1600b-cf9d-4a64-8764-8d27a5b0260d; ak_bmsc=26B3387093FB95B62A3EE4C1068284C4~000000000000000000000000000000~YAAQJNj2SE7bvc6JAQAAzx6A9RTskzH3Vg8HhDr3AzdVpqeqJOXaCgRKFvtPl2x5vuGt+gS9gDWcE13r7qoP1hEFmdlywcPpYbzE01N8Z/UG/xqeZIDbI4TObnnVRCP+hI02a7B+wV1G17R5xGr5FJ9mK4/flIqxWuH7zSb6eh8iy1/aXBmHSb6E8Oc/xnZOcelfD97gfpJRCXWw+0E2I9c+5gAuMoZcqbTX2efnl796hB8OBTgna+GcXpfSqNugpiwfZlW4F0JhN1pF08O/vZnFyygkDeYChquI8dsfug4YrCMQkuuX0X6nO01BMoyp35pWlQMD09uGePc+JXND8ASfRkE3kBZpg3oq5u0j3JCyvgzJ8uXmKrmuuGmG29yJf7MGyRDVzd22LHHlcucBn5hkfe4x00z+mMhS7RlOZhSGvqLalua2QxPjpf8erW1B5zHYI8tHR51X9jzOdUPOcd/9JX+sVcdwOQuH4eDgR761CK2TeeJmY3gnAE7Edov2+UDczp+wtJGM7L/Sw+iLsH0auGHU; bm_sv=D432F986809346A282755AC1E6AC8056~YAAQJNj2SG3evc6JAQAA/ueC9RRFSUauoM6jtTHuj1ucf0Oy+oPOCJIrJ4dCkzObTyiEdb2BZsrm61ZrpXCm1lDJQUZHAGgZWiKLBFdnwTMjYR3SXPS2BSEHbFGVPKnpIP6LNNnroi/WlIxIVjmJDC5jf3uwf7AIujQBRUIV6ZKaPIg2pYS8ye3/Ep4FjAwfrnCc2WH6p7fdh3//dYuHfNzWn2KownCyNuhHaHwkmHxFnKQ4gfUnSMM1N0fsno/NYA==~1; JSESSIONID=uNY7j2e-zHlkObOOxquFxcx0Tnv8a95G-Gyki6yE.svlpje1g10; JSESSIONID2=Ilr0BgZkWZOdaloTg0mCP71Y8_4QuzfiApTd5jg7.svlpje21g14; MO=P; bm_sv=D432F986809346A282755AC1E6AC8056~YAAQFdwAyfSimb2JAQAAU8Gn9RSeYGU43Q9gCYKBKjp4PuEXz0nB0uxDTaAidBo1lOdesbxuPHEhEqTma/jeG9EPE3HmXi/NfGEoDgrdMepkDE1cKKn/vsT4PMZIN8+/IMYqQhVioGefFxBy5NkP8R9fwo7JeMB3psH7UNvVgYMZqSTsu8EaAhHtuTROU1wtwDBrNnuX1fqbKD5VhPAQZ/ImVm7XBcqE7E/gQxA6ZY6tBAtfBocX0c+Kv9BLAuX4Sg==~1; PJECSID=b05de42ec6f29cc0; PJESID=98bcb5ba410dd2c6',
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

        response = requests.request("GET", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

        payload = "AJAXREQUEST=_viewRoot&fPP%3AnumProcesso-inputNumeroProcessoDecoration%3AnumProcesso-inputNumeroProcesso=&mascaraProcessoReferenciaRadio=on&fPP%3Aj_id147%3AprocessoReferenciaInput=&fPP%3Adnp%3AnomeParte=&fPP%3Aj_id165%3AnomeAdv=&fPP%3Aj_id174%3AclasseProcessualProcessoHidden=&tipoMascaraDocumento=on&fPP%3AdpDec%3AdocumentoParte={}&fPP%3ADecoration%3AnumeroOAB=&fPP%3ADecoration%3Aj_id209=&fPP%3ADecoration%3AestadoComboOAB=org.jboss.seam.ui.NoSelectionConverter.noSelectionValue&fPP=fPP&autoScroll=&javax.faces.ViewState=j_id2&fPP%3Aj_id215=fPP%3Aj_id215&AJAX%3AEVENTS_COUNT=1&".format(self._data['cpf'])
        headers = {
        'authority': 'pje1g.trf3.jus.br',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'PJESID=; PJECSID=; MO=P; JSESSIONID=oZr3ml9dr61KD_zJTkaS0DP4CiJf_ZnyY7PE_54I.svlpje1g10; _ga=GA1.1.581667930.1691522903; _ga_J77T54V192=GS1.1.1691522903.1.0.1691522935.0.0.0; PJECSID=a5f71de4d2bf5fa5; PJESID=e814daa583f455f6; OAuth_Token_Request_State=9ed1600b-cf9d-4a64-8764-8d27a5b0260d; ak_bmsc=26B3387093FB95B62A3EE4C1068284C4~000000000000000000000000000000~YAAQJNj2SE7bvc6JAQAAzx6A9RTskzH3Vg8HhDr3AzdVpqeqJOXaCgRKFvtPl2x5vuGt+gS9gDWcE13r7qoP1hEFmdlywcPpYbzE01N8Z/UG/xqeZIDbI4TObnnVRCP+hI02a7B+wV1G17R5xGr5FJ9mK4/flIqxWuH7zSb6eh8iy1/aXBmHSb6E8Oc/xnZOcelfD97gfpJRCXWw+0E2I9c+5gAuMoZcqbTX2efnl796hB8OBTgna+GcXpfSqNugpiwfZlW4F0JhN1pF08O/vZnFyygkDeYChquI8dsfug4YrCMQkuuX0X6nO01BMoyp35pWlQMD09uGePc+JXND8ASfRkE3kBZpg3oq5u0j3JCyvgzJ8uXmKrmuuGmG29yJf7MGyRDVzd22LHHlcucBn5hkfe4x00z+mMhS7RlOZhSGvqLalua2QxPjpf8erW1B5zHYI8tHR51X9jzOdUPOcd/9JX+sVcdwOQuH4eDgR761CK2TeeJmY3gnAE7Edov2+UDczp+wtJGM7L/Sw+iLsH0auGHU; bm_sv=D432F986809346A282755AC1E6AC8056~YAAQJNj2SG3evc6JAQAA/ueC9RRFSUauoM6jtTHuj1ucf0Oy+oPOCJIrJ4dCkzObTyiEdb2BZsrm61ZrpXCm1lDJQUZHAGgZWiKLBFdnwTMjYR3SXPS2BSEHbFGVPKnpIP6LNNnroi/WlIxIVjmJDC5jf3uwf7AIujQBRUIV6ZKaPIg2pYS8ye3/Ep4FjAwfrnCc2WH6p7fdh3//dYuHfNzWn2KownCyNuhHaHwkmHxFnKQ4gfUnSMM1N0fsno/NYA==~1; JSESSIONID=uNY7j2e-zHlkObOOxquFxcx0Tnv8a95G-Gyki6yE.svlpje1g10; JSESSIONID2=Ilr0BgZkWZOdaloTg0mCP71Y8_4QuzfiApTd5jg7.svlpje21g14; MO=P; bm_sv=D432F986809346A282755AC1E6AC8056~YAAQFdwAyfSimb2JAQAAU8Gn9RSeYGU43Q9gCYKBKjp4PuEXz0nB0uxDTaAidBo1lOdesbxuPHEhEqTma/jeG9EPE3HmXi/NfGEoDgrdMepkDE1cKKn/vsT4PMZIN8+/IMYqQhVioGefFxBy5NkP8R9fwo7JeMB3psH7UNvVgYMZqSTsu8EaAhHtuTROU1wtwDBrNnuX1fqbKD5VhPAQZ/ImVm7XBcqE7E/gQxA6ZY6tBAtfBocX0c+Kv9BLAuX4Sg==~1; PJECSID=b05de42ec6f29cc0; PJESID=98bcb5ba410dd2c6',
        'origin': 'https://pje1g.trf3.jus.br',
        'referer': 'https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        with open(os.path.join(self._data['path'],'esaj.html'),'wb') as f:
            f.write(response.content)
        
        with open(os.path.join(self._data['path'],'esaj.html'),'r') as f:
            html_contente = f.read()
        
        html_contente_modify = html_contente.replace("/cpopg/css/saj/saj-paginacao.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/css/saj/saj-paginacao.css?v=2.8.34-30").replace("/cpopg/js/formulario.js?n=","https://esaj.tjsp.jus.br/cpopg/js/formulario.js?n=").replace("/cpopg/jsp/list.js?n=","https://esaj.tjsp.jus.br/cpopg/jsp/list.js?n=").replace("/cpopg/softheme/src/js/app.js?n=","https://esaj.tjsp.jus.br/cpopg/softheme/src/js/app.js?n=").replace("/cpopg/js/saj/acessibilidade/acessibilidade.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/acessibilidade/acessibilidade.js?n=").replace("/cpopg/js/saj-cpo-cbpesquisa.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj-cpo-cbpesquisa.js?n=").replace("/cpopg/js/saj/saj-numeroProcesso.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-numeroProcesso.js?n=").replace("/cpopg/js/saj/saj-mascara-input.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-mascara-input.js?n=").replace("/cpopg/js/saj/saj-browser.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-browser.js?n=").replace("/cpopg/js/saj/saj-popup-modal-1.0.0-1.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-popup-modal-1.0.0-1.js?n=").replace("/cpopg/js/saj/saj-tooltip.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-tooltip.js?n=").replace("/cpopg/js/saj/saj-web-2.2.41-4.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-web-2.2.41-4.js?n=").replace("/cpopg/js/saj/saj-select2.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-select2.js?n=").replace("/cpopg/webjars/select2/3.5.4/select2_locale_pt-BR.js?n=","https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2_locale_pt-BR.js?n=").replace("/cpopg/js/select2/select2.js?n=","https://esaj.tjsp.jus.br/cpopg/js/select2/select2.js?n=").replace("/cpopg/webjars/lodash/4.17.5/lodash.js?n=","https://esaj.tjsp.jus.br/cpopg/webjars/lodash/4.17.5/lodash.js?n=").replace("/cpopg/js/jquery/jquery.browser.min.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.browser.min.js?n=").replace("/cpopg/js/jquery/jquery.blockUI.min.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.blockUI.min.js?n=").replace("/cpopg/js/jquery/jquery.func_toggle.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.func_toggle.js?n=").replace("/cpopg/js/jquery/jquery.min.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.min.js?n=").replace("/cpopg/css/saj/select2/saj-select2.css","https://esaj.tjsp.jus.br/cpopg/css/saj/select2/saj-select2.css").replace("/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30").replace("/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30").replace("/cpopg/css/formulario.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/css/formulario.css?v=2.8.34-30").replace("/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30").replace("/cpopg/softheme/src/css/app.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/softheme/src/css/app.css?v=2.8.34-30").replace('<footer>\n    <nav class="navbar__footer">\n        <div class="navbar__footer__container">\n\n            <ul class="navbar__footer__list-brand">\n                <li class="navbar__footer__list-brand__item">\n                    <a href="https://www.softplan.com.br/solucoes/saj-tribunais/" class="navbar__footer__list-brand__item__link link_softplan_tribunais">\n                        <img src="https://esaj.tjsp.jus.br/esaj/img/brand/icon-saj.png" alt="SAJ">\n                    </a>\n                </li>\n                <li class="navbar__footer__list-brand__item">\n                    <a href="https://www.softplan.com.br/" class="navbar__footer__list-brand__item__link link_softplan">\n                        <img src="https://esaj.tjsp.jus.br/esaj/img/brand/icon-softplan.png" alt="Softplan">\n                    </a>\n                </li>\n            </ul>\n\n            <ul class="navbar__footer__list-actions">\n            </ul>\n        </div>\n    </nav>\n</footer>','')
        with open(os.path.join(self._data['path'],'esaj.html'),'w', encoding='utf-8') as f:
            f.write(html_contente_modify)
        
        self.navegation.firefox('file:///{}'.format(os.path.join(self._data['path'],'esaj.html')),None)
        self.navegation.screen(self._data['path']+'{}.png'.format(self._archive))
        img_path = self._data['path']+'{}.png'.format(self._archive)
        self.convert(img_path)
        os.system('rm {}'.format(os.path.join(self._data['path'],'esaj.html')))
        self.navegation.close_driver()
                    
        for arquivo in os.listdir(self._data['path']):
            if arquivo.find(self._archive) > -1:
                print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                return
            print('Download concluido')
        
        raise ValueError
    

    def convert(self,pName):
        # storing image path
        img_path = pName
        
        # storing pdf path
        pdf_path = pName.replace('png','pdf')
        
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