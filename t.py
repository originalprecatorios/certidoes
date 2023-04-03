import requests
from recaptcha.captcha import Solve_Captcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from PIL import Image
import img2pdf
import requests

captcha = Solve_Captcha()
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
teste = response.text.split('__RequestVerificationToken')[1].split('/>')[0].split('value=')[1].replace('"','').strip()
response = captcha.recaptcha('6Le_CtAZAAAAAEbTeETvetg4zQ7kJI0NH5HNHf1X','https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao')


url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Gerar"

payload='Tipo=CIVEL&TipoDeDocumento=CPF&Documento=403.154.468-54&Nome=Wesley Silva Cabral de Oliveira&NomeSocial=&Abrangencia=SJSP&g-recaptcha-response={}&__RequestVerificationToken={}'.format(response,teste)
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

print(response.text)

texto_formatado = response.text.replace('<img src="/certidao-regional/imagens/trf3logo2.png" />','<img src="https://web.trf3.jus.br/certidao-regional/imagens/trf3logo2.png" />').replace('<img src="/certidao-regional/imagens/trf3brasao.png" />','<img src="https://web.trf3.jus.br/certidao-regional/imagens/trf3brasao.png" />').replace('<main role="main" class="pb-3">\r\n\r\n\r\n<div class="container">\r\n\r\n        <a class="btn btn-primary float-left" href="/certidao-regional">Página inicial</a>\r\n\r\n    <div class="row">    \r\n        <div class="col-md-4 offset-md-8 float-right">\r\n                <button id="botaoImprimirCertidao" class="btn btn-primary float-left">\r\n                    Imprimir certidão\r\n                </button>\r\n        </div>\r\n    </div>\r\n</div>\r\n\r\n','')
with open('/opt/projetos/original/certidoes/templates/response_css.text') as arquivo:
  dado = arquivo.read()
with open('arquivo.html', 'w') as f:
    f.write(texto_formatado)
    f.write(f'<style>{dado}</style>')
fp = webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
driver = webdriver.Firefox(firefox_profile=fp)
driver.get('file:///opt/projetos/original/certidoes/arquivo.html')
driver.get_full_page_screenshot_as_file('teste.png')
img_path = 'teste.png'
        
# storing pdf path
pdf_path = 'teste.png'.replace('png','pdf')

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