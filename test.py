from selenium import webdriver

CHROME_PATH = None
CHROMEDRIVER_PATH = None

chrome_options = webdriver.chrome.options.Options() 
chrome_options.add_argument("--headless")  
if CHROME_PATH:
    chrome_options.binary_location = CHROME_PATH
if CHROMEDRIVER_PATH:
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
else:
    driver = webdriver.Chrome(options=chrome_options)

driver.get('https://threatfeeds.io/')
items = driver.find_elements_by_css_selector('div.name')
for item in items:
    print(item.text)

driver.close()
