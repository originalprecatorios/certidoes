import requests
from bs4 import BeautifulSoup
from recaptcha.captcha import Solve_Captcha

cap = Solve_Captcha()

url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao"

payload={}
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Referer': 'https://web.trf3.jus.br/certidao-regional/',
  'Cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8AU8fK4sDwRFuLeYMUvoVK4ILxVzahkJNYLsHs9VHaOg8VsJ1GOg6gB-I7Gu__xOJqYcifAn14eJkutlBtiMCX3y2NFd_67kLK7TGx_VI-Ryc19ZQA0UtC6LSPtA8WV6Y0LbT-8BpA2MU6KfkiSnA1s; __utma=138416428.1408847584.1658335800.1665690557.1677276536.8; __utmz=138416428.1658335800.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.1408847584.1658335800; ak_bmsc=3FE51110E3BE6E494B5E4E91936B4FE5~000000000000000000000000000000~YAAQDN4AyeXVGHiGAQAA4th4hRLBeaB6T6TxOBKOnFdhXbR5qjrf6Aph7iy61WRbrj9UzQXJxp148gAulZ6Q94usfZC75OKkicslMCtlqQmvgv00xI1ql/R8iF0iJOHdhqyrR6EmuurIHNUF7b+ZLDAWwgquookuOkNDb6VlW1fJlniqXD8OL51R1OvQbPX2CfJgTfv/uLRbf/LweMoGvjtokp5j21iiUMmkwMRxEroMTZyITeQLGt4ZIjL9a0gbKyVJG5+nBlwzNfbEoemzO990AZgwSbWIH1DPro+tJ3DLcS+FpSJ4dQCo9usmdHG91dv9vWMu0UPjHg/JgdARmetBKCF2GBIRz0cGprIMD1JShh2+8JMM4/u02mZJd0G3ZqFqR0+MrFfpOKD7dDLWnCcnzQJM/+QNLmlCBabTTdSB1/iiMVo4B7k97//YShP7vg==; bm_mi=7EFAB80244941899AA898D292BFBE068~YAAQDN4AyeLVGHiGAQAAp5V4hRKdFDM6ZIGTirt8YF98gBJ1yKNFHz4F9TyYVIxdkRtoYrf0IsCamb3vw/nzFOhW9R73Uj8kRQXSoyENz5auGM1R1fkdqnILGRya93S7lxw8DdIlJTcxjB9Z8rbKxunJjHFv8ElGlBtPJWhgGtjfxkIlghLqqpaJxrYgsiZHABrh/mQz4EFX8OvqN9Y4Hk+kY4a5gdx61cbGaGHP0HbTzyx0Ij3qDwzjOJrMdCH5D33H0Yjp2XUtH4ot1we38a37h4c++8o7fMEhZQcR1brkghJJQa9Cfc4lgKKJmzuLOkMajmEUAkiuXhKILhofiLA=~1; bm_sv=F90584A0D8FF53F7378F385C3DF5C82A~YAAQjeDEF2q1aYKGAQAAyHKihRIWkcVSYgzAbbMK4FGZHoDEg9UysJav0Ss/7jjvN93eJEUM88gAC/N7UWxaEBVDZMH14i+6yJLTqdV1lqiwqsaXya0GgXeDEEUdcUjtm+4QxY9yWRXunxjAowZnVVMzNKKW32VvRwPRWyaRYzljDWl4f0bY5DfN/7pBOIQe8kU8cp/WY3WX+qCvesIzVMvla+RRCCifWSYfa288EXIUgj6ENCP2tAXiLDFVfcDTbCA=~1; ASP.NET_SessionId=5ncs0ha1vrsow4emftl1snri; __utmc=138416428; .AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8AU8fK4sDwRFuLeYMUvoVK4OeuI55UgU8i4oIuZCtrF2BfgRNrliDtVc2TLjDvkOYPHSMteF_TfsuewiiaB8I5l1Ykq_p0c4xKuHwnQCbqHX46Q9uTEsAzc8MjZMHF_KCBtMz2JeayYgrxfvZKM0FNU; ak_bmsc=AE3F300EDA67D95996F4637701DD5774~000000000000000000000000000000~YAAQDN4AySrWGHiGAQAAcumIhRJgKYWG9MW3LALDdX1lIglWg3kJpFhUlTSMWK5RjFrrBrFisWHhBbIMhJBV5wnV8Xo9rZZJzZyut7MeSQBwj7qnfnkDNhf58mIeMd4eUUwRDJKEH6w+ccgvWJq9KgjiYFsDkUYxc6i6NRwdjHaQP4+Oee4hbxn5UvBT5IlvCtcmg2nc5dCLv0i6go4g9oPs0x5xtWxcwRXEtysvq5DZ892NhS3e0pRGdT7/8JeS3jjzHRZByS1aKKwDZEk5PZe4NW++gwos/KqEoDaUIEZkGo8rkyqS7a0cb2wEL1SvCN8rhCtsuJ1ZF7gpFQ9lavzMNFjUvVfW5ObcHZbDyf3+EvEAbBSoTirVXZz2m0U=; bm_mi=611573C266F036B86A51D975551B56D7~YAAQDN4AyWjWGHiGAQAAoZyZhRJZOLepf8qBof2v5UoGUposDTDPMbkE9gaiqDwNFIKgKWH74aGKrJCYjAy9p0lI2HZjPpoQ+JwRmTBzOBrRVuUpnTPn6JYdGS9sXn08T5pP4SkqluYX1zLcwPt+I4drDeKLK2ketxGEXw4uiRkkO3aCOR2eHjUJ8ymDKds7dIF1hyUnezM/TPhXv9huEIM0tUjjo5zgQVMR7tA6Gb4kc5iSeFIvLgrvy3u0fNtIdL04g60N38yCCvLFFMLJKetbamdgs0DfVc8boj44qtohVXu56KNZk+IMTINN5ROTEmF5BNYYjEENvX7gShMQDXm8QBiySniUob2QmyzR+jfffhchnZ/8KJs68p574RTB2X+E1g4t3wmYLirzh3Ad2WR6+OSivg==~1; bm_sv=F90584A0D8FF53F7378F385C3DF5C82A~YAAQDN4AyXXWGHiGAQAAGTujhRKraazOlXPwYOjXFHbQpX3L/7hoZK0zKRw44nzq/eslMaSCavGBdvjgHpHFZoZ//wr7SYkouNtVgMvq/XE+mlZq81bjyvRS3/kGJuWsuRK/bHGIdprxJ2EChSUknmXtCB/aEVyWLnuDPWmWVvTXW/sxV58h971/mlXc/47gnK/O9lHLn4yUKFYGsfMQ5HNf+RjcTTWaO6PDZ+t1rfQP84e2bWNDvWiUgusSF9OLF1M=~1',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'TE': 'trailers'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

soup = BeautifulSoup(response.content, 'html.parser')

token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
site_key = '6Le_CtAZAAAAAEbTeETvetg4zQ7kJI0NH5HNHf1X'

response = cap.recaptcha(site_key,'https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao')
url = "https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/Gerar"

payload='Tipo=CRIMINAL&TipoDeDocumento=CPF&Documento=403.154.468-54&Nome=Wesley%2BSilva%2BCabral%2Bde%2BOliveira&NomeSocial=&Abrangencia=SJSP&g-recaptcha-response={}&__RequestVerificationToken={}'.format(response,token)
headers = {
  'authority': 'web.trf3.jus.br',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control': 'max-age=0',
  'content-type': 'application/x-www-form-urlencoded',
  'cookie': '.AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8AU8fK4sDwRFuLeYMUvoVK4ILxVzahkJNYLsHs9VHaOg8VsJ1GOg6gB-I7Gu__xOJqYcifAn14eJkutlBtiMCX3y2NFd_67kLK7TGx_VI-Ryc19ZQA0UtC6LSPtA8WV6Y0LbT-8BpA2MU6KfkiSnA1s; __utma=138416428.1408847584.1658335800.1665690557.1677276536.8; __utmz=138416428.1658335800.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.1408847584.1658335800; ak_bmsc=3FE51110E3BE6E494B5E4E91936B4FE5~000000000000000000000000000000~YAAQDN4AyeXVGHiGAQAA4th4hRLBeaB6T6TxOBKOnFdhXbR5qjrf6Aph7iy61WRbrj9UzQXJxp148gAulZ6Q94usfZC75OKkicslMCtlqQmvgv00xI1ql/R8iF0iJOHdhqyrR6EmuurIHNUF7b+ZLDAWwgquookuOkNDb6VlW1fJlniqXD8OL51R1OvQbPX2CfJgTfv/uLRbf/LweMoGvjtokp5j21iiUMmkwMRxEroMTZyITeQLGt4ZIjL9a0gbKyVJG5+nBlwzNfbEoemzO990AZgwSbWIH1DPro+tJ3DLcS+FpSJ4dQCo9usmdHG91dv9vWMu0UPjHg/JgdARmetBKCF2GBIRz0cGprIMD1JShh2+8JMM4/u02mZJd0G3ZqFqR0+MrFfpOKD7dDLWnCcnzQJM/+QNLmlCBabTTdSB1/iiMVo4B7k97//YShP7vg==; bm_mi=7EFAB80244941899AA898D292BFBE068~YAAQDN4AyeLVGHiGAQAAp5V4hRKdFDM6ZIGTirt8YF98gBJ1yKNFHz4F9TyYVIxdkRtoYrf0IsCamb3vw/nzFOhW9R73Uj8kRQXSoyENz5auGM1R1fkdqnILGRya93S7lxw8DdIlJTcxjB9Z8rbKxunJjHFv8ElGlBtPJWhgGtjfxkIlghLqqpaJxrYgsiZHABrh/mQz4EFX8OvqN9Y4Hk+kY4a5gdx61cbGaGHP0HbTzyx0Ij3qDwzjOJrMdCH5D33H0Yjp2XUtH4ot1we38a37h4c++8o7fMEhZQcR1brkghJJQa9Cfc4lgKKJmzuLOkMajmEUAkiuXhKILhofiLA=~1; bm_sv=F90584A0D8FF53F7378F385C3DF5C82A~YAAQjeDEF2q1aYKGAQAAyHKihRIWkcVSYgzAbbMK4FGZHoDEg9UysJav0Ss/7jjvN93eJEUM88gAC/N7UWxaEBVDZMH14i+6yJLTqdV1lqiwqsaXya0GgXeDEEUdcUjtm+4QxY9yWRXunxjAowZnVVMzNKKW32VvRwPRWyaRYzljDWl4f0bY5DfN/7pBOIQe8kU8cp/WY3WX+qCvesIzVMvla+RRCCifWSYfa288EXIUgj6ENCP2tAXiLDFVfcDTbCA=~1; ASP.NET_SessionId=5ncs0ha1vrsow4emftl1snri; __utmc=138416428; .AspNetCore.Antiforgery.gubY14yPxpQ=CfDJ8AU8fK4sDwRFuLeYMUvoVK4OeuI55UgU8i4oIuZCtrF2BfgRNrliDtVc2TLjDvkOYPHSMteF_TfsuewiiaB8I5l1Ykq_p0c4xKuHwnQCbqHX46Q9uTEsAzc8MjZMHF_KCBtMz2JeayYgrxfvZKM0FNU; ak_bmsc=AE3F300EDA67D95996F4637701DD5774~000000000000000000000000000000~YAAQDN4AySrWGHiGAQAAcumIhRJgKYWG9MW3LALDdX1lIglWg3kJpFhUlTSMWK5RjFrrBrFisWHhBbIMhJBV5wnV8Xo9rZZJzZyut7MeSQBwj7qnfnkDNhf58mIeMd4eUUwRDJKEH6w+ccgvWJq9KgjiYFsDkUYxc6i6NRwdjHaQP4+Oee4hbxn5UvBT5IlvCtcmg2nc5dCLv0i6go4g9oPs0x5xtWxcwRXEtysvq5DZ892NhS3e0pRGdT7/8JeS3jjzHRZByS1aKKwDZEk5PZe4NW++gwos/KqEoDaUIEZkGo8rkyqS7a0cb2wEL1SvCN8rhCtsuJ1ZF7gpFQ9lavzMNFjUvVfW5ObcHZbDyf3+EvEAbBSoTirVXZz2m0U=; bm_mi=611573C266F036B86A51D975551B56D7~YAAQDN4AyWjWGHiGAQAAoZyZhRJZOLepf8qBof2v5UoGUposDTDPMbkE9gaiqDwNFIKgKWH74aGKrJCYjAy9p0lI2HZjPpoQ+JwRmTBzOBrRVuUpnTPn6JYdGS9sXn08T5pP4SkqluYX1zLcwPt+I4drDeKLK2ketxGEXw4uiRkkO3aCOR2eHjUJ8ymDKds7dIF1hyUnezM/TPhXv9huEIM0tUjjo5zgQVMR7tA6Gb4kc5iSeFIvLgrvy3u0fNtIdL04g60N38yCCvLFFMLJKetbamdgs0DfVc8boj44qtohVXu56KNZk+IMTINN5ROTEmF5BNYYjEENvX7gShMQDXm8QBiySniUob2QmyzR+jfffhchnZ/8KJs68p574RTB2X+E1g4t3wmYLirzh3Ad2WR6+OSivg==~1; bm_sv=F90584A0D8FF53F7378F385C3DF5C82A~YAAQDN4AyXXWGHiGAQAAGTujhRKraazOlXPwYOjXFHbQpX3L/7hoZK0zKRw44nzq/eslMaSCavGBdvjgHpHFZoZ//wr7SYkouNtVgMvq/XE+mlZq81bjyvRS3/kGJuWsuRK/bHGIdprxJ2EChSUknmXtCB/aEVyWLnuDPWmWVvTXW/sxV58h971/mlXc/47gnK/O9lHLn4yUKFYGsfMQ5HNf+RjcTTWaO6PDZ+t1rfQP84e2bWNDvWiUgusSF9OLF1M=~1',
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