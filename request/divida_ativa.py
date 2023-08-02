import requests
import os

class Divida_ativa():
    def __init__(self,pData,pCaptcha):
        self.print_colored("Executando a classe Divida_ativa", "blue")
        self._data = pData
        self._captcha = pCaptcha
        self._pasta = self._data['path']
        if os.path.isdir(f'{self._pasta}'):
            self.print_colored("O diretório já existe!", "red")
            print("O diretório existe!")
        else:
            self.print_colored("O Diretório foi criado!", "green")
            os.makedirs(f'{self._pasta}')

    def get_download(self):
        self.print_colored("Função get_download", "blue")
        self.print_colored("Capturando cookie de sessão e chave do captcha", "yellow")
        response = requests.get('https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf')
        JSESSIONID = response.cookies.get('JSESSIONID')
        sitekey = response.text.split('data-sitekey=')[1].split('"')[1]
        self.print_colored("Resolvendo captcha", "yellow")
        resposta = self._captcha.recaptcha(sitekey,'https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf;jsessionid=72B376078823BBC593503156E614391E.395015-sc-03')

        url = "https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf"

        payload='emitirCrda=emitirCrda&emitirCrda%3AcrdaInputCnpjBase=&emitirCrda%3AcrdaInputCpf={}&g-recaptcha-response={}&emitirCrda%3Aj_id97=Emitir&javax.faces.ViewState=j_id1'.format(self._data['cpf'],resposta)
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID={};'.format(JSESSIONID),
        'Origin': 'https://www.dividaativa.pge.sp.gov.br',
        'Referer': 'https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf?param=150304',
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

        self.print_colored("Verificando resposta do servidor", "yellow")
        if response.headers.get("content-type") == "application/pdf":
            with open(os.path.join(self._data['path'],'17- DIVIDA ATIVA.pdf'), "wb") as pdf_file:
                pdf_file.write(response.content)
            self.print_colored("Arquivo PDF salvo com sucesso.", "green")
            
        for arquivo in os.listdir(self._data['path']):
                if arquivo.find('17- DIVIDA ATIVA.pdf') > -1:
                    print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                    return
        self.print_colored("Não foi possivel salvar o arquivo PDF", "red")
        raise ValueError

    def print_colored(self, text, color):
        colors = {
            'blue': '\033[94m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'green': '\033[92m'
        }

        end_color = '\033[0m'

        if color.lower() in colors:
            colored_text = colors[color.lower()] + text + end_color
            print(colored_text)
        else:
            print("A cor selecionada não existe")