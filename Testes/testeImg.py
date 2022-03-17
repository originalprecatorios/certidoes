from myclass.gb import Cut
from myclass.captcha import Captcha

a = Cut()
test = a.crop('./codigo.png')

r = Captcha(test,"")
r._resolve_img()