import requests
from recaptcha.captcha import Solve_Captcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

fp = webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
driver = webdriver.Firefox(firefox_profile=fp)
driver.get('https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao')
time.sleep(2)
captcha = Solve_Captcha()
response = captcha.recaptcha('6Le_CtAZAAAAAEbTeETvetg4zQ7kJI0NH5HNHf1X','https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao')
teste = driver.find_element(By.NAME,'__RequestVerificationToken').get_attribute('value')


url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Gerar"

payload='Tipo=CIVEL&TipoDeDocumento=CPF&Documento=403.154.468-54&Nome=Wesley%2BSilva%2BCabral%2Bde%2BOliveira&NomeSocial=&Abrangencia=SJSP&g-recaptcha-response={}&__RequestVerificationToken={}'.format(response,teste)
headers = {
  'authority': 'web.trf3.jus.br',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control': 'max-age=0',
  'content-type': 'application/x-www-form-urlencoded',
  'cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ={}; __utmz=138416428.1658941714.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.2106690254.1658941714; __utma=138416428.2106690254.1658941714.1658941714.1665690419.2; ak_bmsc={}; bm_sv=D049CF103C81DCF5235C84BC7AC066BA~YAAQv7wQAlJAnZuGAQAAgilItxML+bLUwQ9louFyb8lb+nstlDEPeTCkfO+wdjBc6YYSGsvZzUIENv9dZGqNluzsCWwCpWsoxAao2ybwnMiKY9EbN8h/kdIrcgpNzRBgZCDtGhlYVfQhPbvLWgJlGAKJizewia//OdqhfeIIL3o5q8IZiaEBrySVX66BtyoEodD6m8hwLSzyyZRneBsaZF3mWQRBAN4IrjLICYnihNwO+JEZke/Kpt55DIgmnPVdsw==~1; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8AU8fK4sDwRFuLeYMUvoVK5PTlLR7nlrUJ1waukZWGu22-m9Ot0lIYkTmUssFW4mjsRd2LB_myhVLku9qnw0lLp6y3GKKPUvDT-07Xan6_6o9gfdZGKySWO719XM_XeeYGI8OX3D7aIgCx5PsU_HJOYb3h_TeDbN1URPtpPrsamf0q64SRcwc-vvyo5yJim45fiimAqpz8CVfoC8ijHRtw7QJm9bbBIks3WGJ6Z01TxGcsaouIASl8X7Xi-MoCCz2g29gniXy5XC1t0yS1F1kVOstVUyO1af3dlYVqmik4kOmvBWuiRh6aouKmkRlsJPTDYU5wFcNORu6anZSDWwL_IJc-jHTQFEzf9HjGqXsMw1hEKxeI_-4wXvPCEBe8q_YA'.format(driver.get_cookies()[0]['value'],driver.get_cookies()[1]['value']),
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