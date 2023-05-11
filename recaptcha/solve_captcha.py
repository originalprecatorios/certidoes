from colorama import init, Fore, Style
from selenium import webdriver
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import os
import time

"""Colorama module constants."""
init(convert=True)  # Init colorama module.
red = Fore.RED  # Red color.
green = Fore.GREEN  # Green color.
yellow = Fore.YELLOW  # Yellow color.
reset = Style.RESET_ALL  # Reset color attribute.




class hCaptcha:

    def __init__(self,processo, pLink,pInstancia, pError) -> None:
        self.processo = processo
        self._link = pLink
        self._instancia = pInstancia
        self.extension_path = 'assets/Tampermonkey.crx'
        self.driver = self.webdriver()  # Start new webdriver.
        self._error = pError
        self._error._getcoll('error')

    def webdriver(self):
        try:
            """Start webdriver and return state of it."""
            options = webdriver.ChromeOptions()  # Configure options for Chrome.
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
            options.add_argument('user-agent={0}'.format(user_agent))
            options.add_extension(self.extension_path)  # Add extension.
            options.add_argument("--lang=en-US")  # Set webdriver language
            options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            options.add_argument('log-level=3')  # No logs is printed.
            options.add_argument('--mute-audio')  # Audio is muted.
            options.add_argument("--enable-webgl-draft-extensions")
            options.add_argument("--ignore-gpu-blocklist")
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()  # Maximize window to reach all elements.
            return driver
        
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self.processo,
                    'sistema': 'trf3',
                    'erro': e.msg,
                    'funcao' : 'erro na função webdriver',
            }
            self._error.addData(err)
            return

    def element_clickable(self, element: str) -> None:
        try:
            """Click on element if it's clickable using Selenium."""
            WDW(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, element))).click()
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self.processo,
                    'sistema': 'trf3',
                    'erro': e.msg,
                    'funcao' : 'erro na função element_clickable',
            }
            self._error.addData(err)
            return

    def element_visible(self, element: str):
        try:
            """Check if element is visible using Selenium."""
            return WDW(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, element)))
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self.processo,
                    'sistema': 'trf3',
                    'erro': e.msg,
                    'funcao' : 'erro na função element_visible',
            }
            self._error.addData(err)
            return

    def window_handles(self, window_number: int) -> None:
        try:
            """Check for window handles and wait until a specific tab is opened."""
            WDW(self.driver, 30).until(lambda _: len(self.driver.window_handles) == window_number + 1)
            # Switch to asked tab.
            self.driver.switch_to.window(self.driver.window_handles[window_number])
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self.processo,
                    'sistema': 'trf3',
                    'erro': e.msg,
                    'funcao' : 'erro na função window_handles',
            }
            self._error.addData(err)
            return

    def download_userscript(self) -> None:
        try:
            cont = 0
            while True:
                if cont <= 9:
                    """Download the hCaptcha solver userscript."""
                    try:
                        print('Installing the hCaptcha solver userscript.', end=' ')
                        self.window_handles(1)  # Wait that Tampermonkey tab loads.
                        self.driver.get('https://greasyfork.org/en/scripts/425854-hcaptcha-solver-automatically-solves-hcaptcha-in-browser')
                        # Click on "Install" Greasy Fork button.
                        self.element_clickable('//*[@id="install-area"]/a[1]')
                        # Click on "Install" Tampermonkey button.
                        self.window_handles(2)  # Switch on Tampermonkey install tab.
                        #self.element_clickable('//*[@value="Install"]')
                        self.element_clickable('//*[@id="input_SW5zdGFsYXJfdW5kZWZpbmVk_bu"]')
                        self.window_handles(1)  # Switch to Greasy Fork tab.
                        self.driver.close()  # Close this tab.
                        self.window_handles(0)  # Switch to main tab.
                        print(f'{green}Installed.{reset}')
                        break
                    except TE:
                        print(f'{red}Failed.{reset}')
                        cont += 1
                        continue
                else:
                    break
        
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self.processo,
                    'sistema': 'trf3',
                    'erro': e.msg,
                    'funcao' : 'erro na função download_userscript',
            }
            self._error.addData(err)
            return
                
                

    def demonstration(self) -> None:
        try:
            """Demonstration of the hCaptcha solver."""
            cont = 0
            while True:
                if cont <= 9:
                    try:
                        links = []
                        self.driver.get(self._link)
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso"))).send_keys(self.processo)
                        self.driver.execute_script('window.scrollBy(0, 100)')
                        self.driver.delete_all_cookies()
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "fPP:searchProcessos"))).click()
                        self.driver.delete_all_cookies()
                        time.sleep(10)

                        for t in range (0,100):
                            texto = self.driver.find_element_by_id('fPP:processosTable').text.split('resultados encontrados')[0].split('\n')[2].strip()
                            if texto != '':
                                print(f'{red}Solve HCaptcha.{reset}')
                                time.sleep(1)
                                break
                            else:
                                print('realizando hcaptcha')
                                time.sleep(5)
                                continue



                        #WDW(self.driver, 100).until(EC.visibility_of_element_located((By.CLASS_NAME, 'text-muted')))
                        #WDW(self.driver, 600).until(lambda _: len(self.element_visible('//*[@id="fPP:processosTable:j_id219"]/div/span')))
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "fPP:processosTable:tb")))
                        listas = self.driver.find_element_by_id('fPP:processosTable:tb').find_elements_by_tag_name('tr')
                        for lista in range(len(listas)):
                            link = listas[lista].find_elements_by_tag_name('a')[0].get_attribute('onclick').split(',')[1].replace(')','').replace("'","")
                            links.append(f'https://pje{self._instancia}g.trf3.jus.br/'+link)
                        print(f'{green}Solved.{reset}')
                        self.driver.close()
                        return links
                    except:
                        print(f'{red}Error.{reset}')
                        self.driver.delete_all_cookies()
                        cont += 1
                        continue
                else:
                    break
        
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self.processo,
                    'sistema': 'trf3',
                    'erro': e.msg,
                    'funcao' : 'erro na função demonstration',
            }
            self._error.addData(err)
            return