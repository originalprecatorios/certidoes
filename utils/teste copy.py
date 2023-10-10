import requests
from recaptcha.captcha import Solve_Captcha
import os
from PIL import Image
import pdfkit
import requests
import time
import io
import httpx
from weasyprint import HTML
import requests
import base64
from bs4 import BeautifulSoup

def load_captcha():
    url = "https://duc.prefeitura.sp.gov.br/certidoes/pgImagem.ashx"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=2moy0v3uvpy2lcj3xylbwmws; ServerID=rd4o00000000000000000000ffff0a0a4459o443; SWCookieConfig={"aceiteSessao":"S","aceitePersistentes":"S","aceiteDesempenho":"S","aceiteEstatisticos":"S","aceiteTermos":"S"}; _ga=GA1.1.733918143.1692967001; _ga_LC6GL9KCK4=GS1.1.1692967000.1.1.1692967028.0.0.0; TS01b2d78c=0181a10bc7258a639d750528327d5d2601d1d723666232b1e0ef20f2b4a17b57943963f9ec843bb83b1bde9bf3a45540d4ddcedef260ca1e5f1bddcf41b21fc75ee7e78da30b8a93e8db8b58d7736cf83ab3848384; TS3592777f029=083a958c66ab2800ed894d85f151163c6ab347dfae522a3fdb841838aae00717f0efe8273dfedb28955df3d09f02bd37; TSPD_101=083a958c66ab2800a80e622117e6c16f898dc79d500b8a99aca5a8813e917b7b0bda249b2adc15be14baf3ea95f0b99e089069b98e051800dc5fd395131420cdf3de12ed0b156b3dfbe86f3802284862; TS9a5d5ac3027=083a958c66ab20009956fa7cd55e68ba310722c93c7436d7c31d6056dbe8552c593ebca41a2061a008edb0191e1130005c7832232d581ba1ec7221c0efe6a1bdf5e24ea80d1c313ea640eb4d7e5170ff84c61d40961c3bd9ec29055fe8f05923; TS3592777f077=083a958c66ab28004009df2433bd3ccf217e5d430f852fabb8c3539073e05a17a798c5dd311ddd2c6224bcbf9ce1e9e5082f8fab661720002dc8f8a873f8c1dadb5d6a9906e3a6ae3b94932e82fea9d2dd8aee63e0450304; ASP.NET_SessionId=kba3oe2xhlwyav0xoj2b03is; ServerID=rd4o00000000000000000000ffff0a0a4459o443; TS01b2d78c=0181a10bc79a4f087da264e2bf28c773ebeb4d2991810d2d0fc5881f603578cfcf396496cd82126d2eb5d3e5d45edc2fd36c642bd421d1ad52a0e07c4673a2e85d6aef77c07fcaec0a8ad4b70ca861daf9603f5c01; TS3592777f029=083a958c66ab2800edafdbd86da061e2fe260482d0e88e3287536b4d73d26b7a734f2f178fa5b2af788bdd920e3ff2b7; TS9a5d5ac3027=083a958c66ab20006c218a5d21c1061ea2ebda30a83f0654ce8c78a60cc915bb70acde1c50307a5f08bdbb78db113000c09dc9c8876e4e6ccb68e3eada847dcad93b5d5c0001f1594ffe1019415e88d8c86d17332b9467a1839534106387c3c9; TSPD_101=083a958c66ab28001276b9174db727d49f8d0c977aa8ac85a421571b4894ba411e7f27374af4aa94c3a462c304ec5ef9084dfc56370518000635e06dbca64a2db0670ecd9408ab774f29f86acc1fe506',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
        }
    imagem_captcha = requests.request("GET", url, headers=headers, verify=False)
    url = "https://duc.prefeitura.sp.gov.br/certidoes/forms_anonimo/frmConsultaEmissaoCertificado.aspx"

    payload={}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'ASP.NET_SessionId=2moy0v3uvpy2lcj3xylbwmws; ServerID=rd4o00000000000000000000ffff0a0a4459o443; SWCookieConfig={"aceiteSessao":"S","aceitePersistentes":"S","aceiteDesempenho":"S","aceiteEstatisticos":"S","aceiteTermos":"S"}; _ga=GA1.1.733918143.1692967001; _ga_LC6GL9KCK4=GS1.1.1692967000.1.1.1692967028.0.0.0; TS01b2d78c=0181a10bc7258a639d750528327d5d2601d1d723666232b1e0ef20f2b4a17b57943963f9ec843bb83b1bde9bf3a45540d4ddcedef260ca1e5f1bddcf41b21fc75ee7e78da30b8a93e8db8b58d7736cf83ab3848384; TS3592777f029=083a958c66ab2800ed894d85f151163c6ab347dfae522a3fdb841838aae00717f0efe8273dfedb28955df3d09f02bd37; TSPD_101=083a958c66ab2800a80e622117e6c16f898dc79d500b8a99aca5a8813e917b7b0bda249b2adc15be14baf3ea95f0b99e089069b98e051800dc5fd395131420cdf3de12ed0b156b3dfbe86f3802284862; TS9a5d5ac3027=083a958c66ab20009956fa7cd55e68ba310722c93c7436d7c31d6056dbe8552c593ebca41a2061a008edb0191e1130005c7832232d581ba1ec7221c0efe6a1bdf5e24ea80d1c313ea640eb4d7e5170ff84c61d40961c3bd9ec29055fe8f05923; TS3592777f077=083a958c66ab28004009df2433bd3ccf217e5d430f852fabb8c3539073e05a17a798c5dd311ddd2c6224bcbf9ce1e9e5082f8fab661720002dc8f8a873f8c1dadb5d6a9906e3a6ae3b94932e82fea9d2dd8aee63e0450304; ASP.NET_SessionId=kba3oe2xhlwyav0xoj2b03is; ServerID=rd4o00000000000000000000ffff0a0a4459o443; TS01b2d78c=0181a10bc79a4f087da264e2bf28c773ebeb4d2991810d2d0fc5881f603578cfcf396496cd82126d2eb5d3e5d45edc2fd36c642bd421d1ad52a0e07c4673a2e85d6aef77c07fcaec0a8ad4b70ca861daf9603f5c01; TS3592777f029=083a958c66ab2800edafdbd86da061e2fe260482d0e88e3287536b4d73d26b7a734f2f178fa5b2af788bdd920e3ff2b7; TS9a5d5ac3027=083a958c66ab20006c218a5d21c1061ea2ebda30a83f0654ce8c78a60cc915bb70acde1c50307a5f08bdbb78db113000c09dc9c8876e4e6ccb68e3eada847dcad93b5d5c0001f1594ffe1019415e88d8c86d17332b9467a1839534106387c3c9; TSPD_101=083a958c66ab28001276b9174db727d49f8d0c977aa8ac85a421571b4894ba411e7f27374af4aa94c3a462c304ec5ef9084dfc56370518000635e06dbca64a2db0670ecd9408ab774f29f86acc1fe506',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    soup = BeautifulSoup(response.content,'html.parser')

    tokencac = soup.find(id='ctl00_ConteudoPrincipal_consentimento___tokencac').get('value')
    ct = soup.find(id='ctl00_hdnUrlDefault').get('value')
    view = soup.find(id='__VIEWSTATE1').get('value')
    view1 = soup.find(id='__VIEWSTATE').get('value')
    generation = soup.find(id='__VIEWSTATEGENERATOR').get('value')

    url = "https://duc.prefeitura.sp.gov.br/certidoes/forms_anonimo/frmConsultaEmissaoCertificado.aspx"

    payload='PageProdamSPOnChange=&PageProdamSPPosicao=Form%3D0%3B0%2F&PageProdamSPFocado=ctl00_ConteudoPrincipal_ddlTipoCertidao&__EVENTTARGET=ctl00%24ConteudoPrincipal%24ddlTipoCertidao&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATEFIELDCOUNT=2&__VIEWSTATE=iT6jLsUQtaDi4bsBR777GRIw0Gy594PUPV8LQ%2BXadHpuGuYYJBwHcD5ZaQ1An4m9aJ%2BNcLTkREUcDAZvgr1qQTxbl%2BKHPNiaXODFl8Ijt53NlChhdob08mqPIQEZh0T1tX%2Bmo9csg1vJRyyHs5Pwt%2FDr876cbfjc2vs2wwcwHeWuS9I3pviGoij6l8K%2B2FNsCTd3SJU0aAqin7UjDQk%2B6k2dJo8BHLhYy13k%2BHFFa2m9CCkc1NNFVVDNclgYhM38%2FhQeOhrV0osmUpfvP7eQ%2ByNB%2BU5tAgX%2FzsQTR%2Fz3XinjYk%2BT4uU1lPN7Poy9wX9x%2FgJ6hPAeFN1W6UfM%2Bf6OcqnXWXlbLHa0LuTjNZINZKFiFb%2BLeA9CEQSokQZdNZ3WPyCEYCmLrPl7uxJ6BFim6ZdnqjDvaFiS8cYn3DdQTduB%2BQROJxkPBpJN4iarqSrFVIKJTC9WF3euzUo3fCcqwVUIZ1ATaXCv8UdZIsn%2FMynnvnk2Ngb1Xj9rGLTtFcDJkcm4UfropXMOGtXUpb645LL8H4jpNhM8MYxjXQTi6jJBLxlbkriNlTkpXaxh0YIlcO2k2gTrnVtEJrXAiiD%2Fy%2B8WgzhqHyhPSZajSvtMD93Hu%2BMFauFlqmNI0T99qRMwfx74JUwh0g6jMQjqlLgxp7ijCbRAtDaOlYvuQ3hefIOCXioMGZNFypfX8ImTsmJRDWRotKQbqAVQ0JlQzgUo%2B4sOlmavdAEd0v0OmpUwJKDf8SoeioewTvLCozWxdKH65opCILdyNuc7nubqwUcZj9z3QITir%2FbfveOgxCDdTHwp8zEiSMTwAj6oVJEhpS3VxliuRzfD%2FUIdGy63rQJ%2BZNIg1UVChEsjvhrJcpTefiQ%2FEzRoc9cgfcjtZ%2BbZgV8IIGZSxyu8Hh5qqKWD72wgUZt23Yc2XNbKIxlvwADrq8nP%2F6ECmVQ885vfCKysa7gfh0DvzeCzOBvwaHZSTWETrxnDDKf9kgr2yJx3Jh8ul6LVFSzc91CwcKIj2iHwkfKL&__VIEWSTATE1=sEgLlIFzt8pMEX8VD2O96E3DwpuSPd7tp%2FXeWJENgvWTEFKApG%2F%2Fz9uemlvuYeJ860OR8Q%3D%3D&__VIEWSTATEGENERATOR=786373C9&__VIEWSTATEENCRYPTED=&ctl00%24ConteudoPrincipal%24hdnParmCertidao=&ctl00%24ConteudoPrincipal%24__tpAudio=mp3&ctl00%24ConteudoPrincipal%243130540=&ctl00%24ConteudoPrincipal%24ddlTipoCertidao=1&ctl00%24ConteudoPrincipal%24consentimento%24__contribuinte=&ctl00%24ConteudoPrincipal%24consentimento%24__tipoContribuinte=&ctl00%24ConteudoPrincipal%24consentimento%24__tokencac=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6WyJTRjk0MjFJIiwidXN1YXJpbyBkZSBpbnRlZ3JhY2FvIHNlbmhhIHdlYiAtIHNmOTQyMWkiXSwiaHR0cDovL3NjaGVtYXMucHJvZGFtLnNwLmdvdi5ici9zdHMvY2xhaW1zL0xvZ2luIjoic2Y5NDIxaSIsImh0dHA6Ly9zY2hlbWFzLnByb2RhbS5zcC5nb3YuYnIvc3RzL2NsYWltcy9TaXN0ZW1hIjoic2Y5NDIxIiwiaHR0cDovL3NjaGVtYXMucHJvZGFtLnNwLmdvdi5ici9zdHMvY2xhaW1zL0hpZXJhcnF1aWEiOiJ7XCJjZHNlbmhhcGFkcmFvXCI6bnVsbCxcImNkdXN1YXJpb1wiOm51bGwsXCJjaWhpZXJhcnF1aWF1c3VhcmlvXCI6MTk5ODU1LFwiY2loaWVyYXJxdWlhdXN1YXJpb2FsdGVyYWNhb1wiOjAsXCJjaWhpZXJhcnF1aWF1c3VhcmlvaW5jbHVzYW9cIjowLFwiY2l1c3VhcmlvXCI6MTEyNTM2LFwiY29kaWdvaGllcmFycXVpYVwiOjE0OTYsXCJjb2RpZ29oaWVyYXJxdWlhcGFpXCI6bnVsbCxcImR0YWx0ZXJhY2FvXCI6bnVsbCxcImR0aW5jbHVzYW9cIjpudWxsLFwiaW5hZG1pbmlzdHJhZG9yaGllcmFycXVpYVwiOmZhbHNlLFwibm9tZWhpZXJhcnF1aWFcIjpcIndlYnNlcnZpY2UgY29udHJvbGUgZGUgaW50ZWdyYWNhb1wiLFwibnJvcmRlbVwiOjAsXCJzaWdsYWhpZXJhcnF1aWFcIjpcIndzaVwifSIsImFkZnMxZW1haWwiOiJ0ZWNvcnJlYUBwcm9kYW0uc3AuZ292LmJyIiwiaHR0cDovL3NjaGVtYXMucHJvZGFtLnNwLmdvdi5ici9zdHMvY2xhaW1zL01vZGVsb0F1dG9yaXphY2FvIjoiMCIsImh0dHA6Ly9zY2hlbWFzLnByb2RhbS5zcC5nb3YuYnIvc3RzL2NsYWltcy9SZWN1cnNvcyI6ImtoTUFBQitMQ0FBQUFBQUFCQURObUUxdjFEQVFoditLbFJOSXEwaEZYT0JudE53UWg0azkyYnB5NHVDUEZJSDYzenYrMkNRcnA0c0tCK2UyR3R2SjQ5ZHZac2I3L1UvRHRaQm4vU0N0d3dHYXI2eXgvWmZQbis2YUUyc01jbStzWG9OdE43VWN4SVRXaG5HQmxodkpJYzZnT0Zobk5CUEl3Z1FOY2M0c3JaeFJoUm5PZUd4T3pTTjBVa2tIUW0rQ1hIeVRrNzVmWDNqWHZKeitHYTRGNWRxcEx4Z3BqQVlNSzFsWlQ1d2NLaE0vdllmNHlSc3BxakxMMGU2cG5GbUoraURhUnM1UzI0S3p2cUpjRStybHJFdGdHdlhLd1k0YktuNXJCbFdiYk1vMWxubUJoc0ZwSXlQc091K3lCNUQyRUx1WVFVa0Jwc0RQOFFOSWJwK0RQWHA1M3ZNRmhYMFdWbWhtY1h5RVoreHFFYlo1YktkS0xLaVFER0d0SDUyMkRObGxUWDM2Q1F3TVNJZjlkLzUxYWwzZEJTb3NqUkdqQWJVU1VNcG5FNXBCN2txWnNsa2F0OEc3a3piTVd3K1VMcW9pRzV6TVRpNWJrTk00amc1R2x6NjVpdFMyVS9ybnp0bkh1TWVVZWFNMXE5RWxWY0hoS0VnMGZGdllEWFZ5dzlXYU91d2Jwb09ySEJvZHBYZjB2UzdDUVZJNVlNeTdIemhNRUV0d1dQaXhIbnRvSTdhbmYzc1BoL0VKdFJCeTdEVVplQzZJdHdOMWtPSzFncGlVUE1PN2FobXdEaXhXN2N5V1BjVGNRZVRMdTI3V2trakx1QjdJRXA2YXQ5OTVlOHR5WUtObWxZNkcvTDZraUtzTjVQSlJzWU9JYjA1YTR5K091V25ZVjFuUlUwT3VabmxtK01uUk9OblRWQ3FHOUdhaVZGVTNRWVRPMzNCS0d0K1U3bU5vYjNEVzU5c2V6N3hybzh5dUZ0VkFEOG43eld2cm1yZ3hpRTZQbGp4WkpsOEJZeW1xV0Q0dmV3Z2lsamZBSEdmYWsrKzcrRzhNOEpCbUFuRnhGdjlKLytNVmdaZWgyWklUQUFBPSIsInJvbGUiOiJueE1BQUIrTENBQUFBQUFBQkFDZFdNbU80ellRdmVjckNKOFNZR2JBUlJ2ekVUbmtHZ1NOTWttN09iQkVOaWs1UVlMOGUwcVNQVDB3MmlCcmZHcTQ3WHBrVmIxRi91UGZnL0V2cjk0bFNHK0xoNWR6V21JNC9Nb09MWmZ5OE9rd2plOXZnWEU1QndhQlpaOW5Od0w3eXgxSGlPd3p5eWZkREQxK1B2dDVBUVBiNTMvNy9mRGZwNmNBU3FqaFk0Q2Z2a013WVAxMEF4QU5DVUNydG4xeUE1WmNuaGxFejhZdytUa2tQNTBSNnJnQkRiM1VSS0JPUFcyVmdUaWJWMkF4QlFzakFzU28rWGJ6ZW9CK2FFUnhGbkIwYVY0U3R1d1ZSckFocjVkSlFpdEZ2VXdGMW9VTDN2Z1Z3V2NURWcxQlNGNUd3SDVkZ1ZsLzlqTmNHTXNYTGptdGE1bzMxVGdKZDhFR3ZNK3kzb3lJbzlybjQvK0djNFdMWCt2dEc5QVROMENMcHN6R0kyVEhyR054L1Fma2ZabmJnYmJNU3JYbCtSL3Q2Y2JKbmtaNkxkVXpUbjVmZmR5cmQ3d2xubDJVSi83ak5CY1YrMlRBc0hoWk10dlVaWnYxTUFnU3pvQ3ZDaHdMbXk1YXFUaXR2dXlhcGx6ZmpMZjk2VHBhZFYxeit2dUVHMGxVSjk1V25OMVpqNHBodVJTMENXTm55aXd6S2VDM2JzZm5rdHFjc2xTZ1RlUzdwMjVLU2FwZmJvKzl4THMwMEU3ZmRSWENiUmR6TzN0RHE0NjIwQmVybjhCZzVyZ0JkRFR0d2VtV20rL2p2R3psV3lGb3E0bmx5OUkybmR5OTkwUURrS284MlNsY3cvc05VRDVwMUIyMExrdC9kRzk3OVZiUlpBZTNwOXgrbEV1bFd3UXdFemlpQzFkTU55Wm5ZSTE3ZXpveVptUEN4TFdnZFVweldSYTU1TjRXbC96b3BqbXNTWm50Y2kwRWtkTmRSYnpJOXE1SUxXMHF5THJ5VGJJNzJUM3I3UlIzelAzdHpMS21tUlBtUDZEYWFKa24yVTJ2OEsxcHF4Q0tGelRVQjZEU3ZwVVpzOGtJZVkvTEpySFcxYlRIbFVIek12dnllZDVXZGhZOXA1VkhhOURsOHQ2ZDd1R0l4Z2pWdERYbHo1L1IybjZlanBkZkVNWXVuRXFHb1NaZElBeXNKblFGM2hLenZOS2JacGJxai9qVXNObmNWNjRWOGFtVTl4WHI3ek9Zc0ZrRnBwaUdUT21hVWVTQVBwb25ETFhVa04xWDZKSFAvNFExbjVySUZhZjVkRnNqcnZtcmxNMkFBR0NKN1ZmbERJT09NSEM1cHZjVVpwZm5RQk9JdHNLcTgzS1BlQjJSeDExYklUL1h1eDAwdE41M3ZYamNIUXgwWDZ6THh3dkdYdWVKcmVqRjR5alhjbU9ZL1RWazRtOGd3K085dHo5V04zcHZBRVR3OHk2UWU5cWpqSzEveko4ZkFNeWV1RzlDUGdvS2pvVnpMcjZ3YzRvdkllSjNiRWp1bzI3OCtUOWs3NC9jbnhNQUFBPT0iLCJuYmYiOjE2OTMyMjcwMTQsImV4cCI6MTY5MzIyNzYxNCwiaWF0IjoxNjkzMjI3MDE0LCJpc3MiOiJodHRwOi8vY2FjcGx1cy5wcm9kYW0iLCJhdWQiOiJodHRwOi8vNjU3MTMzODktMWMyYy00YWMwLWE3YzktMTU2MzlhNjZjNmIxIn0.G58F3gVV6-KsLv0hrs2ARYe-zUbzdjB7K4Tcr2DG7vo&ctl00%24hdnUrlDefault=%2Fcertidoes%2FDefault.aspx%2FVerificaJanejaSessao'
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=2moy0v3uvpy2lcj3xylbwmws; ServerID=rd4o00000000000000000000ffff0a0a4459o443; SWCookieConfig={"aceiteSessao":"S","aceitePersistentes":"S","aceiteDesempenho":"S","aceiteEstatisticos":"S","aceiteTermos":"S"}; _ga=GA1.1.733918143.1692967001; _ga_LC6GL9KCK4=GS1.1.1692967000.1.1.1692967028.0.0.0; TS01b2d78c=0181a10bc7258a639d750528327d5d2601d1d723666232b1e0ef20f2b4a17b57943963f9ec843bb83b1bde9bf3a45540d4ddcedef260ca1e5f1bddcf41b21fc75ee7e78da30b8a93e8db8b58d7736cf83ab3848384; TSPD_101=083a958c66ab2800444cc1e428eb05f29070a587a2d9ef1b3861930bd3c87b328c96b2de04ead803bd7983f4f2d5f77908f2613701051800ce25624ad79bb6bdb0670ecd9408ab774f29f86acc1fe506; TS9a5d5ac3027=083a958c66ab2000028d95468105819fecf146743a4559ac3dba11064e08d90f5e0ddfaa59f33f8008179a7201113000e390e4e4d5a5c986110830ad5e2395420f35d88814727f3dd6d89e4c87cce8f04d062b1396ff02831e58ac910aa780a3; TS3592777f077=083a958c66ab28006705fcf1f829575cc09037e524102ddeba1feb5a4666996adcb465b6d037398da07550f9cf4bf8be08329dfac1172000c07f8e9d1c8f4d7fdb5d6a9906e3a6ae4e4aa2c02b2e9e50a5993b61c9bbea41; ASP.NET_SessionId=kba3oe2xhlwyav0xoj2b03is; ServerID=rd4o00000000000000000000ffff0a0a4459o443; TS01b2d78c=0181a10bc75fc390d110aa4f72befa78c955f911a75a135c29eeacdc49150ab9c05f72d35f5aed9a4adc5678f2c707814b2076c8c7b0b0dbf05915df07f1d25561ac9fbaf33374cf34253fe6ce73fba5c6c9de6eb5; TS3592777f029=083a958c66ab28007267209268f2fa4b1db8bf019e50d40d15e8ccc9e7da13a1a5f064bceae8b1583276bf6838ebfc63; TS9a5d5ac3027=083a958c66ab20008a2cec6069c5a86023520377de5775b41eaea74483e1b6da5efa22df34d98dd10872453c7a1130009b55cbb5527c8ebac42228b934cce530bfea94e6260325381178e332f5b9ada7a71323489566d0934b809aff14ca9315; TSPD_101=083a958c66ab28001276b9174db727d49f8d0c977aa8ac85a421571b4894ba411e7f27374af4aa94c3a462c304ec5ef9084dfc56370518000635e06dbca64a2db0670ecd9408ab774f29f86acc1fe506',
    'Origin': 'https://duc.prefeitura.sp.gov.br',
    'Referer': 'https://duc.prefeitura.sp.gov.br/certidoes/forms_anonimo/frmConsultaEmissaoCertificado.aspx',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)











































    with open('novo 2.html', 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    modified_html = html_content.replace(
        'name="fPP:dpDec:documentoParte" />\n',
        'name="fPP:dpDec:documentoParte" value="403.154.468-54"/>\n'
    )
    with open('saida.html', 'w', encoding='utf-8') as modified_html_file:
        modified_html_file.write(modified_html)
    HTML('saida.html').write_pdf('testefinal.pdf')

    response = requests.get('https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam;jsessionid=sDa7m2nvdIFKn2hh9hdj6iRlAtknaA9PBF7z7K24.srvpje1gcons04')
    cookies = response.cookies.get_dict()

    url = "https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam;jsessionid={}".format(cookies['JSESSIONID'])

    payload = "AJAXREQUEST=_viewRoot&fPP%3AnumProcesso-inputNumeroProcessoDecoration%3AnumProcesso-inputNumeroProcesso=&mascaraProcessoReferenciaRadio=on&fPP%3Aj_id151%3AprocessoReferenciaInput=&fPP%3Adnp%3AnomeParte=&fPP%3Aj_id169%3AnomeAdv=&fPP%3Aj_id178%3AclasseProcessualProcessoHidden=&tipoMascaraDocumento=on&fPP%3AdpDec%3AdocumentoParte=403.154.468-54&fPP%3ADecoration%3AnumeroOAB=&fPP%3ADecoration%3Aj_id213=&fPP%3ADecoration%3AestadoComboOAB=org.jboss.seam.ui.NoSelectionConverter.noSelectionValue&fPP=fPP&autoScroll=&javax.faces.ViewState=j_id1&fPP%3Aj_id219=fPP%3Aj_id219&AJAX%3AEVENTS_COUNT=1&"
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID={}; ; JSESSIONID=NQFHaJHYJMjxDJAplxu5XnzUrSL6D5XwV1ov0FQb.srvpje1gcons02; OAuth_Token_Request_State=7b4f26d6-3b59-48aa-b236-892fee5b5651'.format(cookies['JSESSIONID']),
    'Origin': 'https://pje1g.trf1.jus.br',
    'Referer': 'https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    teste  = response.text.replace('/consultapublica/stylesheet/estilos/bootstrap/bootstrap.min.css','estilos/bootstrap.min.css').replace('/consultapublica/stylesheet/dropzone/dropzone.min.css','estilos/dropzone.min.css').replace('/consultapublica/stylesheet/estilos/richfaces/tema.min.css','estilos/tema.min.css').replace('/consultapublica/stylesheet/padrao.min.css','estilos/padrao.min.css').replace('/consultapublica/stylesheet/autos-digitais.min.css','estilos/autos-digitais.min.css').replace('/consultapublica/js/modernizr.custom.min.js','estilos/modernizr.custom.min.js').replace('/consultapublica/js/jquery-ui-1.8.1.min.custom.js','estilos/jquery-ui-1.8.1.min.custom.js').replace('/consultapublica/js/jquery-2.1.4.min.js','estilos/jquery-2.1.4.min.js').replace('/consultapublica/js/bootstrap/bootstrap.min.js','estilos/bootstrap.min.js').replace('/consultapublica/js/jquery.maskedinput.min.js','estilos/jquery.maskedinput.min.js').replace('/consultapublica/js/mousetrap/mousetrap.min.js','estilos/mousetrap.min.js').replace('/consultapublica/js/mousetrap/plugins/global-bind/mousetrap-global-bind.min.js','estilos/mousetrap-global-bind.min.js').replace('/consultapublica/js/pje/menu.min.js','estilos/menu.min.js').replace('/consultapublica/js/global.min.js','estilos/global.min.js').replace('/consultapublica/js/pje.js','estilos/pje.js').replace('/consultapublica/js/pjeOffice.js','estilos/pjeOffice.js').replace('/consultapublica/js/signerApplet.js','estilos/signerApplet.js')
    with open('teste.html', 'wb') as f:
        f.write(teste.encode('utf-8'))
    HTML('teste.html').write_pdf('testefinal.pdf')

    str(soup).replace('/consultapublica/a4j/g/3_3_3.Final/org/ajax4jsf/framework.pack.js','estilo/framework.pack.js').replace('/consultapublica/a4j/g/3_3_3.Final/org/richfaces/ui.pack.js','estilo/ui.pack.js').replace('/consultapublica/a4j/s/3_3_3.Finalorg/richfaces/renderkit/html/css/basic_classes.xcss/DATB/eAELXT5DOhSIAQ!sA18_;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/basic_classes.xcss').replace('/consultapublica/a4j/s/3_3_3.Finalorg/richfaces/renderkit/html/css/extended_classes.xcss/DATB/eAELXT5DOhSIAQ!sA18_;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/extended_classes.xcss').replace('/consultapublica/a4j/s/3_3_3.Final/org/richfaces/skin.xcss/DATB/eAELXT5DOhSIAQ!sA18_;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/skin.xcss').replace('/consultapublica/stylesheet/estilos/bootstrap/bootstrap.min.css;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/bootstrap.min.css').replace('/consultapublica/stylesheet/dropzone/dropzone.min.css;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/dropzone.min.css').replace('/consultapublica/stylesheet/estilos/richfaces/tema.min.css;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/tema.min.css').replace('/consultapublica/stylesheet/padrao.min.css;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/padrao.min.css').replace('/consultapublica/stylesheet/autos-digitais.min.css;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/utos-digitais.min.css').replace('/consultapublica/js/modernizr.custom.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/modernizr.custom.min.js').replace('/consultapublica/js/jquery-ui-1.8.1.min.custom.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/min.custom.js').replace('/consultapublica/js/jquery-2.1.4.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/min.js').replace('/consultapublica/js/bootstrap/bootstrap.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/bootstrap.min.js').replace('/consultapublica/js/jquery.maskedinput.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/maskedinput.min.js').replace('/consultapublica/js/mousetrap/mousetrap.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/mousetrap.min.js').replace('/consultapublica/js/mousetrap/plugins/global-bind/mousetrap-global-bind.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/mousetrap-global-bind.min.js').replace('/consultapublica/js/pje/menu.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/menu.min.js').replace('/consultapublica/js/global.min.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/global.min.js').replace('/consultapublica/js/pje.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/pje.js').replace('/consultapublica/js/pjeOffice.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/pjeOffice.js').replace('/consultapublica/js/signerApplet.js;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/signerApplet.js').replace('/consultapublica/img/favicon/apple-touch-icon-57x57.png','estilo/apple-touch-icon-57x57.png').replace('/consultapublica/img/favicon/apple-touch-icon-60x60.png','estilo/apple-touch-icon-60x60.png').replace('/consultapublica/img/favicon/apple-touch-icon-72x72.png','estilo/apple-touch-icon-72x72.png').replace('/consultapublica/img/favicon/apple-touch-icon-76x76.png','estilo/apple-touch-icon-76x76.png').replace('/consultapublica/img/favicon/apple-touch-icon-114x114.png','estilo/apple-touch-icon-114x114.png').replace('/consultapublica/img/favicon/apple-touch-icon-120x120.png','estilo/apple-touch-icon-120x120.png').replace('/consultapublica/img/favicon/apple-touch-icon-144x144.png','estilo/apple-touch-icon-144x144.png').replace('/consultapublica/img/favicon/apple-touch-icon-152x152.png','estilo/apple-touch-icon-152x152.png').replace('/consultapublica/img/favicon/apple-touch-icon-180x180.png','estilo/apple-touch-icon-180x180.png').replace('/consultapublica/img/favicon/favicon-32x32.png','estilo/favicon-32x32.png').replace('/consultapublica/img/favicon/favicon-194x194.png','estilo/favicon-194x194.png').replace('/consultapublica/img/favicon/favicon-96x96.png','estilo/favicon-96x96.png').replace('/consultapublica/img/favicon/android-chrome-192x192.png','estilo/favicon/android-chrome-192x192.png').replace('/consultapublica/img/favicon/favicon-16x16.png','estilo/favicon-16x16.png').replace('/consultapublica/img/favicon/manifest.json','estilo/favicon/manifest.json').replace('/consultapublica/img/favicon/safari-pinned-tab.svg','estilo/safari-pinned-tab.svg').replace('/consultapublica/stylesheet/estilos/font-awesome/v5.11.2/css/all.min.css','estilo/all.min.css').replace('/consultapublica/stylesheet/estilos/font-awesome/v5.11.2/css/v4-shims.min.css','estilo/v4-shims.min.css').replace('/consultapublica/img/favicon/mstile-144x144.png','estilo/mstile-144x144.png').replace('/consultapublica/img/pjeMini.png','estilo/pjeMini.png').replace('/consultapublica/img/pje2-branco.png;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/pje2-branco.png').replace('/consultapublica/img/pjeMini.png;jsessionid=_SZ-7UQntp9JNg1NftzpLd4UpAr0lS6McdVeMIDP.srvpje1gcons04','estilo/pjeMini.png')

    captcha = Solve_Captcha()
    resposta = captcha.resolve_hcaptcha('4a65992d-58fc-4812-8b87-789f7e7c4c4b','https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir')
    url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

    payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=R48j9Oo3CDFf%2FjqgaTvosq%2BfqHFmcGDLJ04OGzgk%2BMmJBSPBnmvilTwk8mHEMSTJM4DenQXh3M%2BhpOzZQGqvTMbrAx%2B7Xw%2BpkoEhY0agcQYv0esRs9ptlDtKQSCEyiMtHonv29dqNYZ2VskDlcTzLALvUuHoW88f34Sf8XgzWibeRp5Wo6%2FpSkdcr68hYLGFU3y4Yjo%2BEDSyrB0q9iBEJT3LqSNVAoQ5Dfq0eMZa6sKi%2FT3toQmYIodldsCw0GUJ4U80YW5Lhtg3s5PBeVgIYeSZOyky2DsnviojRvaOwTYbrEHfBABg047QZvy0VzMrPDVGMrw%2BT8rSWTPHTNUbpg5NivM9u%2F8q0cvKL4eKypiutEeCRuK9zBj7a5t0nz9CAvAsF7EQinYgjP8ZiUaWGoP%2F7jHSS9L%2Bu%2FXmCuDaR3Q2ByDaavWuspv0Bid3SOOVcywt7g%3D%3D&__VIEWSTATEGENERATOR=1C0B1C53&__EVENTVALIDATION=mcKH9PmY7J%2FN7q0lULNNbrsUBz4NpZLG2naZxTA5GqPokRnQmZWKF1IqK5484mBwrx7n2A%2BprVcmBe9rSNNE9r0yVjdoa5MrMvMdDbo7x1M2ZeDsx40O5WRUz4fq%2FcTzCYkIvD%2B1Zk01dyTTHLvKRfgaZjpE9wJOGmEtuLQvOOiwsAWP%2BAOen1viyhg%2BbblV%2B%2BmQ5g%3D%3D&ctl00%24MainContent%24grupoDocumento=cpfradio&ctl00%24MainContent%24txtDocumento=403.154.468-54&ctl00%24MainContent%24btnPesquisar=%2BEmitir%2B&g-recaptcha-response={}&ctl00%24MainContent%24hdgrecaptcha={}'.format(resposta,resposta)
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

    url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

    payload={}
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
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.content,'html.parser')
    __VIEWSTATE = soup.find(id='__VIEWSTATE').get('value').replace('/','%2F').replace('+','%2B').replace('=','%3D')
    __VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR').get('value')
    __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get('value').replace('/','%2F').replace('+','%2B').replace('=','%3D')

    captcha = Solve_Captcha()
    resposta = captcha.recaptcha('6LdoPeUUAAAAAIC5yvhe7oc9h4_qf8_Vmq0xd9GU','https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx')

    url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx"

    payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24MainContent%24grupoDocumento=cpfradio&ctl00%24MainContent%24txtDocumento=403.154.468-54&ctl00%24MainContent%24btnPesquisar=%2BEmitir%2B&g-recaptcha-response={}&ctl00%24MainContent%24hdgrecaptcha={}'.format(__VIEWSTATE,__VIEWSTATEGENERATOR,__EVENTVALIDATION,resposta,resposta)
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

    soup = BeautifulSoup(response.content,'html.parser')
    __VIEWSTATE = soup.find(id='__VIEWSTATE').get('value').replace('/','%2F').replace('+','%2B').replace('=','%3D')
    __VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR').get('value')
    __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get('value').replace('/','%2F').replace('+','%2B').replace('=','%3D')


    url = "https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/ImpressaoCertidaoNegativa.aspx"

    payload='__EVENTTARGET=ctl00%24MainContent%24btnImpressao&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}'.format(__VIEWSTATE,__VIEWSTATEGENERATOR,__EVENTVALIDATION)
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=zydipx5n45rvzshk2urlj1ug',
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

    response = requests.request("GET", url, headers=headers, data=payload)

    url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

    payload = "AJAXREQUEST=_viewRoot&fPP%3AnumProcesso-inputNumeroProcessoDecoration%3AnumProcesso-inputNumeroProcesso=&mascaraProcessoReferenciaRadio=on&fPP%3Aj_id147%3AprocessoReferenciaInput=&fPP%3Adnp%3AnomeParte=&fPP%3Aj_id165%3AnomeAdv=&fPP%3Aj_id174%3AclasseProcessualProcessoHidden=&tipoMascaraDocumento=on&fPP%3AdpDec%3AdocumentoParte=403.154.468-54&fPP%3ADecoration%3AnumeroOAB=&fPP%3ADecoration%3Aj_id209=&fPP%3ADecoration%3AestadoComboOAB=org.jboss.seam.ui.NoSelectionConverter.noSelectionValue&fPP=fPP&autoScroll=&javax.faces.ViewState=j_id2&fPP%3Aj_id215=fPP%3Aj_id215&AJAX%3AEVENTS_COUNT=1&"
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

    response = requests.request("POST", url, headers=headers, data=payload)
    'nEHJRN0BzmahNg-nZvcYDBOZqL19VVXOCa8dDKTw.srvpje1gcons01'


    response = requests.get('https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam')

    with open('teste.html','wb') as f:
        f.write(response.content)
    
    with open('teste.html','r') as f:
        html_contente = f.read()
    
    html_contente_modify = html_contente.replace("/cpopg/css/saj/saj-paginacao.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/css/saj/saj-paginacao.css?v=2.8.34-30").replace("/cpopg/js/formulario.js?n=","https://esaj.tjsp.jus.br/cpopg/js/formulario.js?n=").replace("/cpopg/jsp/list.js?n=","https://esaj.tjsp.jus.br/cpopg/jsp/list.js?n=").replace("/cpopg/softheme/src/js/app.js?n=","https://esaj.tjsp.jus.br/cpopg/softheme/src/js/app.js?n=").replace("/cpopg/js/saj/acessibilidade/acessibilidade.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/acessibilidade/acessibilidade.js?n=").replace("/cpopg/js/saj-cpo-cbpesquisa.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj-cpo-cbpesquisa.js?n=").replace("/cpopg/js/saj/saj-numeroProcesso.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-numeroProcesso.js?n=").replace("/cpopg/js/saj/saj-mascara-input.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-mascara-input.js?n=").replace("/cpopg/js/saj/saj-browser.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-browser.js?n=").replace("/cpopg/js/saj/saj-popup-modal-1.0.0-1.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-popup-modal-1.0.0-1.js?n=").replace("/cpopg/js/saj/saj-tooltip.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-tooltip.js?n=").replace("/cpopg/js/saj/saj-web-2.2.41-4.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-web-2.2.41-4.js?n=").replace("/cpopg/js/saj/saj-select2.js?n=","https://esaj.tjsp.jus.br/cpopg/js/saj/saj-select2.js?n=").replace("/cpopg/webjars/select2/3.5.4/select2_locale_pt-BR.js?n=","https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2_locale_pt-BR.js?n=").replace("/cpopg/js/select2/select2.js?n=","https://esaj.tjsp.jus.br/cpopg/js/select2/select2.js?n=").replace("/cpopg/webjars/lodash/4.17.5/lodash.js?n=","https://esaj.tjsp.jus.br/cpopg/webjars/lodash/4.17.5/lodash.js?n=").replace("/cpopg/js/jquery/jquery.browser.min.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.browser.min.js?n=").replace("/cpopg/js/jquery/jquery.blockUI.min.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.blockUI.min.js?n=").replace("/cpopg/js/jquery/jquery.func_toggle.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.func_toggle.js?n=").replace("/cpopg/js/jquery/jquery.min.js?n=","https://esaj.tjsp.jus.br/cpopg/js/jquery/jquery.min.js?n=").replace("/cpopg/css/saj/select2/saj-select2.css","https://esaj.tjsp.jus.br/cpopg/css/saj/select2/saj-select2.css").replace("/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30").replace("/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30").replace("/cpopg/css/formulario.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/css/formulario.css?v=2.8.34-30").replace("/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30").replace("/cpopg/softheme/src/css/app.css?v=2.8.34-30","https://esaj.tjsp.jus.br/cpopg/softheme/src/css/app.css?v=2.8.34-30")
    with open('teste.html','w', encoding='utf-8') as f:
        f.write(html_contente_modify)

    with open('teste.html', 'rb') as f:
        html_content = f.read()
    
    # Defina o tamanho da página em pixels (1366x283)
    page_size = (1366, 283)

    # Criar um objeto HTML
    html = HTML(string=html_content)

    pdf = html.render()

    # Salva o PDF no arquivo de saída
    with open('teste.pdf', 'wb') as output_pdf:
        pdf.write_pdf(output_pdf)

    # Salvar o arquivo PDF
    html.write_pdf('teste.pdf')

    JSESSIONID = response.cookies.get('JSESSIONID')


    response = requests.get('https://cndt-certidao.tst.jus.br/inicio.faces')
    viewstate = response.text.split('javax.faces.ViewState:0" value="')[1].split('"')[0]
    jd_id = 'j_id_jsp_'+response.text.split('name="j_id_jsp_')[1].split('"')[0]

    url = "https://cndt-certidao.tst.jus.br/api"

    payload={}
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID={}; 7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR;'.format(response.cookies.get_dict()['JSESSIONID'],response.cookies.get_dict()['7aa721eeaef392956e2c4add5997cdb0']),
    'Referer': 'https://cndt-certidao.tst.jus.br/inicio.faces;jsessionid={}'.format(response.cookies.get_dict()['JSESSIONID']),
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    token_desafio = data["tokenDesafio"]

    imagem_bytes = bytes((x & 0xFF for x in data["imagem"]))
    imagem_base64 = base64.b64encode(imagem_bytes).decode("utf-8")

    return token_desafio, imagem_base64

token, imagem_base64 = load_captcha()
print("Token Desafio:", token)
print("Imagem em Base64:", imagem_base64)
image_data = base64.b64decode(imagem_base64)
image = Image.open(io.BytesIO(image_data))
image.save('output_image.png')


import requests

url = "https://cndt-certidao.tst.jus.br/inicio.faces"

payload='j_id_jsp_992698495_2=j_id_jsp_992698495_2&j_id_jsp_992698495_2%3Aj_id_jsp_992698495_3=Emitir%2BCertid%C3%A3o&javax.faces.ViewState={}'.format(viewstate.replace('/','%2F').replace('+','%2B').replace('=','%3D'))
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'JSESSIONID={}; 7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR;'.format(response.cookies.get_dict()['JSESSIONID'],response.cookies.get_dict()['7aa721eeaef392956e2c4add5997cdb0']),
  'Origin': 'https://cndt-certidao.tst.jus.br',
  'Referer': 'https://cndt-certidao.tst.jus.br/inicio.faces',
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

print(response.text)
























import requests

url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

payload={}
headers = {
  'authority': 'pje1g.trf3.jus.br',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control': 'max-age=0',
  'cookie': 'MO=P; JSESSIONID2=dXmdUdwG2KvCAazmT5rBbcTVXYGPtfuDhJq0zsPz.svlpje21g14; PJECSID=ebcb5090ef97b5a6; PJESID=3f321c0ad7a8c69a; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQdxY2F9TCnbqJAQAA5Xr9wRQAiZFcJCu58wUsOY7ReD43kP6qypupn5+CEXH++dkvU5Y0icJFmZqNlzDeit2s4ecvl8HVsY3UCAYXPUcodVgtVb9aXmuJZjFjRAT14B/bcBMLLK1CCVmjUUv+MQ18IB9sSU/6Ie/DgGXF9ZBTUM2ulyn+3pqRdIZKG6i8LTArwuLlMEACeoOBODEQydP4c3v7LR1c06hlVnVCW+pdfSEsJxLo768Q/sDhVDFbpuGh/5IMneqWm69bf0qWw4i6UmnqXkwsm4+LwfkEXPh1r71UlcFUYs6MNoIASD8AtPX9rHYa7vEhqeKGAJY41mOauNLk8Ry7O7c16JLVOcnr9cU4deeeYSlPiRH1zZ1rIBczPPAU67ZbKR697V93TxKgEtpVA7Npc73aWOd0bOQxRtx36j0x8QSD/PN4kwLE33SSNVNGqlddZ4nhpOeoEGUJjEaGg4Y/nV36lM5LP0oQWoZSHlvmlaoo; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQdxY2FxfUnbqJAQAAIYAlwhTU3aN+AGsIlvdfcAvScDPViouEZK5h9AEH/i8cV6EMv9zBfcq87gvgyx3EnC3akg80tOlbqLPBre0/V54TSMdzEnWk/chsBCgQyAJWChpYKjoCdmzkIDtdbUxZESmGKIRk/rZsfRMRaiRevzzOjpKYsiyC4NABkwlluO2dzAx+ilE60nkiAcGANi0MeUf9bQG4aa1WMLPXvn+Eu0ruARPJUsUrsgzGiWtCco56iQ==~1; JSESSIONID=prLlPTNHhn9G58YR7SM7pH5QfDXu0uTWZCfqS_am.svlpje1g07; JSESSIONID2=pvb5rRh3E4OeB9tHnkrt19eGIQMzjxS_uxdnVDb3.svlpje21g14; MO=P; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQlNXaF06VnXGJAQAAr0Q9whTK3VOdyl6WFvCaH6H2yb2qfaaSNtXxtW8yz8c8nJcntTgPevs9whmwyFiLZBKcUSi179gePN9ec7ihSg3MMN8EwXTXJbJlcyZNQ8HoMNcuBFcM1NhHChAA4vOw+I/BuVXAmkZy/e9bYis6eLn674wAB+cHYROrt3zE40C3fmVBjvMybV8B4sWRtDYc0lp4iEQPlF7PUGZB1ADFUvbBcxtv4D6/taaTn+9N+V9XHUvt/Gk2T15GSlF1KUhNTLNTrIZA3BQ+7tZ8pQk9rl6/FbAdvg2ir55mvnLIs699PP72iGZ7ROh6QOjy6/lzjjpGc81IIuMCmI7e3ytmpdBN39N4TMSyofUECaF1BQGCgnOAdEsrtOmF4YhBTDFSTmvgLB1GB2HjOmysFr99vaG8KwtDeJOVQ9fhHzTbpcq2jPNp/zeWAaM2LWSFjh+7ojKw5VcAgTrpbrxL9FUGO3T2UPkFgqkhEeYtd/NPHzRseIAVm+IdIG8VeW/uU+kuaXHJUWxA21IaOc1VmnuZpnNr; bm_mi=37A7AD95AA469BB60F7E312E701246AB~YAAQTsQUAqQ3PG6JAQAAKD4AwhSxUihZJgtCjNQVNZTUB0SnVhHclJgZ8pqGgPYayy+C0uYDJTs6J/qb3uxEvFfEn10GxDK6KCZ8F2COtkTSPrf5CRethwXtDuSfGnDQaW04IvN47iWGxpLyyTMRIS8IFkLkfiQLg+nafdkKfss83NxR+lst3UePI0Ai1nXi0lTfiqpHNT8mQ8+NcMraztyoulQFzFWp0pJYaFFwwJI4ZCi05wWrv0i6ROqPW9HxS3aysYwj2S6QXseXZCq3fafSmSd7/oib+SkbcvTW+TS3nUKqk8XVL2IUjC7gJusdnAiNZF6AWKLt+21XNsMZSUp3AEjy1gpCdtFc7Ln0AA==~1; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQlNXaF0+VnXGJAQAAr0Q9whR5Vv+rqu/fsQWqUFF1TObYzfUbRUKJCTeQsNIZ05iguvOPc6c8SYWWGsILQCiL9cKhvWSZsAsSrmkoxWqMPr0FvxeicBTf5qJ7nv1M+2EzhEFZmrZNms/5q0oMTjmgevUMIBBQLkxdYWoSSD7IkjB+La+6oPMtgB4kY3YZL+Z7UiQ5ESy8QYi+6HXS8Jhhk9z8gGJtrYDT9nqzXiQFo+/yIdq2DreFY0kIg/+UpA==~1; PJECSID=29bfdcddb51f695c; PJESID=98bcb5ba410dd2c6',
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

print(response.text)


import requests

url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

payload = "AJAXREQUEST=_viewRoot&fPP%3AnumProcesso-inputNumeroProcessoDecoration%3AnumProcesso-inputNumeroProcesso=&mascaraProcessoReferenciaRadio=on&fPP%3Aj_id147%3AprocessoReferenciaInput=&fPP%3Adnp%3AnomeParte=&fPP%3Aj_id165%3AnomeAdv=&fPP%3Aj_id174%3AclasseProcessualProcessoHidden=&tipoMascaraDocumento=on&fPP%3AdpDec%3AdocumentoParte=000.000.000-00&fPP%3ADecoration%3AnumeroOAB=&fPP%3ADecoration%3Aj_id209=&fPP%3ADecoration%3AestadoComboOAB=org.jboss.seam.ui.NoSelectionConverter.noSelectionValue&fPP=fPP&autoScroll=&javax.faces.ViewState=j_id4&fPP%3Aj_id215=fPP%3Aj_id215&AJAX%3AEVENTS_COUNT=1&"
headers = {
  'authority': 'pje1g.trf3.jus.br',
  'accept': '*/*',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': 'MO=P; JSESSIONID2=dXmdUdwG2KvCAazmT5rBbcTVXYGPtfuDhJq0zsPz.svlpje21g14; PJECSID=ebcb5090ef97b5a6; PJESID=3f321c0ad7a8c69a; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQdxY2F9TCnbqJAQAA5Xr9wRQAiZFcJCu58wUsOY7ReD43kP6qypupn5+CEXH++dkvU5Y0icJFmZqNlzDeit2s4ecvl8HVsY3UCAYXPUcodVgtVb9aXmuJZjFjRAT14B/bcBMLLK1CCVmjUUv+MQ18IB9sSU/6Ie/DgGXF9ZBTUM2ulyn+3pqRdIZKG6i8LTArwuLlMEACeoOBODEQydP4c3v7LR1c06hlVnVCW+pdfSEsJxLo768Q/sDhVDFbpuGh/5IMneqWm69bf0qWw4i6UmnqXkwsm4+LwfkEXPh1r71UlcFUYs6MNoIASD8AtPX9rHYa7vEhqeKGAJY41mOauNLk8Ry7O7c16JLVOcnr9cU4deeeYSlPiRH1zZ1rIBczPPAU67ZbKR697V93TxKgEtpVA7Npc73aWOd0bOQxRtx36j0x8QSD/PN4kwLE33SSNVNGqlddZ4nhpOeoEGUJjEaGg4Y/nV36lM5LP0oQWoZSHlvmlaoo; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQdxY2F0DUnbqJAQAAw5ImwhSLHIffAZgL1S+IibQA9LvNnTurOJbKefwYEVGfs4P9DOP7RDoIOLMcBWtET/sjt9HGSQdRBatRzNUB4VRISVpBCmdmtSU+uReq7bbe/BIzqCWu6mYdK3AagbOHbEXZBf88wqNgcq6AxLxiPJj3+NgztDuj8t6732A+200NWuKFN3ywfIuLOXmehv6i0ET92mTiUi45acIinuayb0GZqbQSkL2YbkjQOLmHWdBdxg==~1; JSESSIONID=prLlPTNHhn9G58YR7SM7pH5QfDXu0uTWZCfqS_am.svlpje1g07; JSESSIONID2=pvb5rRh3E4OeB9tHnkrt19eGIQMzjxS_uxdnVDb3.svlpje21g14; MO=P; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQlNXaF52VnXGJAQAACXU9whSeBK7Mz1T332abnrZc3GbUF5oJVpMu3hTH9vs+svTCDSOynG2AWRQ0LGSGBlGRYrjOxJG/4604VnGZmMc9RBq8SGm6RNtzNq2lnEvgnzH/7Y2gubC1ONyGeYqWfJ/HaAzuGHbOR8rZF2HuubNW/bi4uOO68VIOMJL4gSqNA+xx0AyRIouC9gYvImVdsxlbsOPHLRZ+AB1FgyreT49g06dPNyrz3PCBdXA0Ded2wPwDCnesadmhSD/1A5Ek9euzlYPnGx5wiKxMO9fnlFLZlc7elhHif1hFo0wQgk0bel4OVpuiqowIKbc1Djdzbl0cNoYD3FNEiVZNVjwkvagH9vso3APwW9DjJOB6+9LKpnpUsW61Q+2kYq0rAoD0RGiQFKPTN80oZm+fHKj0vDday7bZlFechnQbXLN0dIPyvs9UuscfFiWWvhN9CKSvGl1tG6Mss0qz/9/UpBmlQtkyORlIQ68OdElBvnL0D8G3r62o36P5xidPgeRkBAnQcr/vq9d15menAGjmjDFxVaft; bm_mi=37A7AD95AA469BB60F7E312E701246AB~YAAQTsQUAqQ3PG6JAQAAKD4AwhSxUihZJgtCjNQVNZTUB0SnVhHclJgZ8pqGgPYayy+C0uYDJTs6J/qb3uxEvFfEn10GxDK6KCZ8F2COtkTSPrf5CRethwXtDuSfGnDQaW04IvN47iWGxpLyyTMRIS8IFkLkfiQLg+nafdkKfss83NxR+lst3UePI0Ai1nXi0lTfiqpHNT8mQ8+NcMraztyoulQFzFWp0pJYaFFwwJI4ZCi05wWrv0i6ROqPW9HxS3aysYwj2S6QXseXZCq3fafSmSd7/oib+SkbcvTW+TS3nUKqk8XVL2IUjC7gJusdnAiNZF6AWKLt+21XNsMZSUp3AEjy1gpCdtFc7Ln0AA==~1; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQlNXaF0+VnXGJAQAAr0Q9whR5Vv+rqu/fsQWqUFF1TObYzfUbRUKJCTeQsNIZ05iguvOPc6c8SYWWGsILQCiL9cKhvWSZsAsSrmkoxWqMPr0FvxeicBTf5qJ7nv1M+2EzhEFZmrZNms/5q0oMTjmgevUMIBBQLkxdYWoSSD7IkjB+La+6oPMtgB4kY3YZL+Z7UiQ5ESy8QYi+6HXS8Jhhk9z8gGJtrYDT9nqzXiQFo+/yIdq2DreFY0kIg/+UpA==~1; PJECSID=29bfdcddb51f695c; PJESID=98bcb5ba410dd2c6',
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

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


























resposta = ''

url = "https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf"

payload='emitirCrda=emitirCrda&emitirCrda%3AcrdaInputCnpjBase=&emitirCrda%3AcrdaInputCpf=403.154.468-54&g-recaptcha-response={}&emitirCrda%3Aj_id97=Emitir&javax.faces.ViewState=j_id1'.format(resposta)
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

captcha = Solve_Captcha()
response = captcha.recaptcha('6Le9EjMUAAAAAPKi-JVCzXgY_ePjRV9FFVLmWKB_','https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf;jsessionid=72B376078823BBC593503156E614391E.395015-sc-03')

url = "https://www2.ssp.sp.gov.br/aacweb/carrega-formulario"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=0000MXy1891S8c64jGyH2HP7kbl:1eirm4393',
    'Referer': 'https://www2.ssp.sp.gov.br/aacweb/carrega-iframe',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
}

# Criar uma instância do cliente HTTP
client = httpx.Client()

# Fazer a requisição usando o método GET
response = client.get(url, headers=headers)

# Verificar o status da resposta
if response.status_code == 200:
    print(response.text)
    sitekey = response.text.split('data-sitekey=')[1].split('\r')[0].replace('"','')
else:
    print(f"Erro {response.status_code} ao fazer a solicitação")

# Fechar a instância do cliente HTTP
client.close()

captcha = Solve_Captcha()
response = captcha.recaptcha(sitekey,'https://www2.ssp.sp.gov.br/aacweb/carrega-formulario')

url = "https://www2.ssp.sp.gov.br/aacweb/emitir-atestado.action"
'''payload = {
    "nome": "ALINE EMILY TIOMI LENSARINI TOMIMURA",
    "numero": "54918611",
    "digito": "6",
    "txtDIAE": "11",
    "txtMESE": "10",
    "txtANOE": "2019",
    "sexo": "F",
    "txtDIA": "24",
    "txtMES": "04",
    "txtANO": "1994",
    "nomePai": "CARLOS TOMOYASHU TOMIMURA",
    "nomeMae": "ROSA MARIA LENSARINI TOMIMURA",
    "g-recaptcha-response": response,  # Adicione o valor correto aqui
    "pesquisa": "Pesquisar"
}'''
payload = {
    "nome": "WESLEY SILVA CABRAL DE OLIVEIRA",
    "numero": "48788239",
    "digito": "8",
    "txtDIAE": "26",
    "txtMESE": "03",
    "txtANOE": "2003",
    "sexo": "M",
    "txtDIA": "14",
    "txtMES": "11",
    "txtANO": "1992",
    "nomePai": "ANTONIO CABRAL DE OLIVEIRA",
    "nomeMae": "JULIENE MARIA DA SILVA",
    "g-recaptcha-response": response,  # Adicione o valor correto aqui
    "pesquisa": "Pesquisar"
}
#payload='nome=WESLEY%20SILVA%20CABRAL%20DE%20OLIVEIRA&numero=48788239&digito=8&txtDIAE=26&txtMESE=03&txtANOE=2003&sexo=M&txtDIA=14&txtMES=11&txtANO=1992&nomePai=ANTONIO%20CABRAL%20DE%20OLIVEIRA&nomeMae=JULIENE%20MARIA%20DA%20SILVA&g-recaptcha-response={}&pesquisa=Pesquisar'.format(response)
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'JSESSIONID=0000MXy1891S8c64jGyH2HP7kbl:1eirm4393',
  'Origin': 'https://www2.ssp.sp.gov.br',
  'Referer': 'https://www2.ssp.sp.gov.br/aacweb/carrega-formulario',
  'Sec-Fetch-Dest': 'iframe',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

try:
    response = httpx.get(url, headers=headers, params=payload)
except:
    time.sleep(5)
    response = httpx.get(url, headers=headers, params=payload)

if response.headers.get("content-type") == "application/pdf":
    with open("arquivo.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    print("Arquivo PDF salvo com sucesso.")
else:
    pdf_file_path = os.path.join('/opt/projetos/original/certidoes','antecedentes.pdf')
    pdfkit.from_string(response.text.replace('/AACWEBSTATIC/img/imp_cab.gif','https://www2.ssp.sp.gov.br/AACWEBSTATIC/img/imp_cab.gif'), pdf_file_path, options={'encoding': 'utf-8'})
    print("Arquivo PDF salvo com sucesso.")
