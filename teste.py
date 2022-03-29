from myclass.firefox import Firefox

dados = {'nome':'gelson luiz ramos pereira junior', 'cpf':'325.044.888-58','genero':'M','nascimento':'08/04/1983','mae':'teresinha lucia da costa ramos pereira'}

p = Firefox(dados)
p._login_esaj()