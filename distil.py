import undetected_chromedriver.v2 as uc
import time
options = uc.ChromeOptions()

# another way to set profile is the below (which takes precedence if both variants are used

# just some options passing in to skip annoying popups
options.add_argument('--no-first-run')
driver = uc.Chrome(options=options, version_main=99)  # version_main allows to specify your chrome version instead of following chrome global version

driver.get('https://nowsecure.nl')  # known url using cloudflare's "under attack mode"

time.sleep(1000)

