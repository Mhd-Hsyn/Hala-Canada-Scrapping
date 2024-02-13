"""
Testing script        HALA CANADA

https://halacanada.info/

"""


import time, json , uuid
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


def get_random_headers():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US, en;q=0.5'
    }
    return headers


headers = get_random_headers()

print("\nMy Random Header is : \n", headers)
print("\n\n")

# for translation
prefs = {
  "translate_whitelists": {"ar":"en"},
  "translate":{"enabled":"true"}
}

# Set Chrome options
options = Options()
# options.headless = False
options.add_argument('--enable-logging')
options.add_argument('--log-level=0')
# options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
options.add_argument(f'user-agent={headers["User-Agent"]}')
options.add_argument('--no-sandbox')
options.add_argument("chrome://settings/")
options.add_argument("--lang=en") 
options.add_argument("--disable-translate")
options.add_experimental_option("prefs", prefs)  # for translation



def sysInit():
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = None
    try:
        print(" *************** Starting Script Hala-Canada Post Scrapping *****************\n")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.maximize_window()
        driver.get("https://halacanada.info/")
        print("\n")

        cancel_btn= driver.find_element(By.ID, "onesignal-slidedown-cancel-button")
        cancel_btn.click()
        time.sleep(2)
        
        accept_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'cmplz-accept'))
            )
        accept_cookies.click()
        
        time.sleep(5)
        driver.refresh()
        time.sleep(5)
        driver.get("https://halacanada.info/")
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        target_span = soup.find('span', class_ ='tdb-logo-img-wrap')
        target_div = soup.find('div', class_= 'td_block_inner td-mc1-wrap')
        if target_span and target_div:
            img = target_span.find('img')
            img_url = img.get('data-src', '')
            print("\nImage URL: ______  ", img_url)

            all_divs = target_div.find_all('div', class_='td_module_flex')
            scraped_data_list = []

            for div in all_divs:
                # Extract data from the div
                image_url = div.find('span', class_='entry-thumb')
                image_url = image_url['data-img-url'] if image_url else ""
                
                title = div.find('h3', class_='entry-title')
                title = title.text.strip() if title else ""
                
                category = div.find('a', class_='td-post-category')
                category = category.text.strip() if category else ""
                
                date = div.find('time', class_='entry-date')
                date = date.text.strip() if date else ""
                
                excerpt = div.find('div', class_='td-excerpt')
                excerpt = excerpt.text.strip() if excerpt else ""

                read_more_link_element = div.find('div', class_='td-read-more')
                read_more_link = read_more_link_element.find('a')['href'] if read_more_link_element else ""

                # Create a dictionary to store the extracted data
                data_dict = {
                    'image_url': image_url,
                    'title': title,
                    'category': category,
                    'date': date,
                    'excerpt': excerpt,
                    'read_more_link': read_more_link
                }

                # Append the dictionary to the list
                scraped_data_list.append(data_dict)

            print("\n\n*************   SOME POSTS  *********************\n\n ")
            
            print(json.dumps(scraped_data_list))
            
            
            print("\n\n")
        else:
            print("\n\nNO HTML FOUND\n\n")
            print(html)
            print("\n\nNO HTML FOUND\n\n")

    finally:
        print("QUIT WEB DRIVER ______________")
        display.stop()
        if driver:
            driver.quit()


sysInit()