from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
firefox_driver = webdriver.Firefox()

firefox_driver.get('http://www.angelfire.com/super/badwebs/')  
scheight = .1
while scheight < 9.9:
    firefox_driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
    scheight += .01        
firefox_driver.save_screenshot('angelfire_firefox.png')