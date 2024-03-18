import requests
import os
from weasyprint import HTML
from utils.selenium_classes import Selenium_classes
import img2pdf
from PIL import Image

class Esaj_busca():
    def __init__(self,pData,pCaptcha,pSelect,pNome):
        print('Esaj Busca')
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
        if self._select == 'NOME':
            response = requests.get('https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta={}&cdForo=-1'.format(self._data['nome']), timeout=self.timeout_seconds)
        else:
            response = requests.get('https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=DOCPARTE&dadosConsulta.valorConsulta={}&cdForo=-1'.format(self._data['cpf'].replace('.','').replace('-','')), timeout=self.timeout_seconds)

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