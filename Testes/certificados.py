# -*- coding: utf-8 -*-
#import pymysql as MySQLdb

import os, string, random

class Certified:
    def __init__(self,quant=30):
        self._checkCert()
        self.alfabeto = string.ascii_letters + string.digits
        self._ret = ''.join(random.choice(self.alfabeto) for i in range(quant))

    def Token(self):
        return self._ret

    def addCert2(self, pFileName, pFolder, pPass):
        certIn = "{0}{1}".format(pFolder, pFileName)
        certKey =  '{0}{1}{2}'.format(pFolder, "key_", pFileName.replace('pfx', 'pem'))
        certOut = certIn.replace('pfx', 'pem')
        certImport = certOut.replace('pem', 'crt')  
        certP12 = certIn.replace('pfx', 'p12')

        commandConvert = "openssl pkcs12 -export -inkey {0} -in {1} -out {2} -passout pass:{3}".format(certIn, certIn, certP12, pPass)
        os.system(commandConvert)

        commandKey = "openssl pkcs12 -in {0} -nocerts -out {1} -nodes -passin pass:{2}".format(certP12, certKey, pPass)
        os.system(commandKey)

        commandCert = "openssl pkcs12 -in {0} -nokeys -out {1} -nodes -passin pass:{2}".format(certP12, certOut, pPass)
        os.system(commandCert)

        return {'key': certKey, 'cert': certOut}
        
        

    def addCert(self, pFileName, pFolder, pPass):
        nickName = self.Token()
        certIn = "{0}{1}".format(pFolder, pFileName)
        certKey =  '{0}{1}{2}'.format(pFolder, "key_", pFileName.replace('pfx', 'pem'))
        certOut = certIn.replace('pfx', 'pem')
        certImport = certOut.replace('pem', 'crt')
        certP12 = certIn.replace('pfx', 'p12')

        commandConvert = "openssl pkcs12 -export -inkey {0} -in {1} -out {2} -passout pass:{3}".format(certIn, certIn, certP12, pPass)
        os.system(commandConvert)

        commandKey = "openssl pkcs12 -in {0} -nocerts -out {1} -nodes -passin pass:{2}".format(certP12, certKey, pPass)
        os.system(commandKey)

        commandCert = "openssl pkcs12 -in {0} -nokeys -out {1} -nodes -passin pass:{2}".format(certP12, certOut, pPass)
        os.system(commandCert)

        commandCrt = "openssl pkcs12 -export -inkey {0} -in {1} -out {2} -name {3} -passout pass:{4}".format(certKey, certOut, certImport, nickName, pPass)
        os.system(commandCrt)

        commandAdd = "pk12util -d sql:$HOME/.pki/nssdb/ -W {0} -i {1}".format(pPass, certImport)
        os.system(commandAdd)

        #Remove temp files
        os.remove(certKey)
        os.remove(certOut)
        os.remove(certImport)
        os.remove(certP12)

        return nickName


    def delCert(self,nickName):
        print('Remove certificate')
        command = "certutil -d sql:$HOME/.pki/nssdb/ -D -n {0}".format(nickName)
        os.system(command)

    def _checkCert(self):
        print('Check cert')
        list_cert = os.popen('certutil -L -d sql:$HOME/.pki/nssdb').read()
        x = list_cert.split('\n')
        for c in x:
                z = c.split(' ')
                if len(z[0]) == 30:
                        self.delCert(z[0])