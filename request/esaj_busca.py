import requests
import os
from weasyprint import HTML

class Esaj_busca():
    def __init__(self,pData,pCaptcha,pSelect,pNome):
        print('Debito Trabalhista')
        self._data = pData
        self._captcha = pCaptcha
        self._select = pSelect
        self._archive = pNome
        if os.path.isdir('{}'.format(self._data['path'])):
            print("O diretório existe!")
        else:
            os.makedirs('{}'.format(self._data['path']))

    def get_download(self):
        if self._select == 'NOME':
            response = requests.get('https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta={}&cdForo=-1'.format(self._data['nome']))
        else:
            response = requests.get('https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=DOCPARTE&dadosConsulta.valorConsulta={}&cdForo=-1'.format(self._data['cpf'].replace('.','').replace('-','')))

        with open(os.path.join(self._data['path'],'esaj.html'),'wb') as f:
            f.write(response.content)
        
        with open(os.path.join(self._data['path'],'esaj.html'),'r') as f:
            html_contente = f.read()
        
        html_contente_modify = html_contente.replace('/cpopg/softheme/src/css/app.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/softheme/src/css/app.css?v=2.8.34-30').replace('/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30').replace('/cpopg/css/formulario.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/css/formulario.css?v=2.8.34-30').replace('/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30').replace('/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30').replace('/cpopg/css/saj/select2/saj-select2.css','https://esaj.tjsp.jus.br/cpopg/css/saj/select2/saj-select2.css')

        with open(os.path.join(self._data['path'],'esaj.html'),'w', encoding='utf-8') as f:
            f.write(html_contente_modify)

        with open(os.path.join(self._data['path'],'esaj.html'), 'rb') as f:
            html_content = f.read()

        # Criar um objeto HTML
        html = HTML(string=html_content)

        # Salvar o arquivo PDF
        html.write_pdf(self._archive)

        os.system('rm {}'.format(os.path.join(self._data['path'],'esaj.html')))
                    
        for arquivo in os.listdir(self._data['path']):
            if arquivo.find(self._archive) > -1:
                print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                return
            print('Download concluido')
        
        raise ValueError