"""
Testing script        HALA CANADA

https://halacanada.info/

"""


import time, json
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



def scrap_links(html):
    all_links = []
    soup = BeautifulSoup(html, 'html.parser')
    main_div = soup.find('div', {'id': 'tdi_67', 'class': 'tdc-zone'})
    all_sub_divs = main_div.find_all('div', {'class': 'wpb_wrapper'}) if main_div else ''
    
    if all_sub_divs:
        for div in all_sub_divs:
            link_ele = div.find_all('div', {'class': 'td-module-thumb'})
            links_list = [link.find('a')['href'] for link in link_ele ]
            all_links.extend(links_list)

    print("\n\n", json.dumps(all_links))

    return all_links




def scrap_data(html):
    data = {
        "title": "",
        "image_url": "",
        "content": ""
    }
    soup = BeautifulSoup(html, 'html.parser')
    title_ele = soup.find('h1', class_='tdb-title-text')
    data['title'] = title_ele.get_text(strip= True) if title_ele else ""
    
    img_div = soup.find('div', {'class': 'tdb_single_featured_image'})
    img_ele = img_div.find('img') if img_div else ""
    data['image_url'] = img_ele['src'] if img_ele and 'src' in img_ele.attrs else ""

    content_div = soup.find('div', class_= 'tdb_single_content')
    content_ele = content_div.find('div', class_='tdb-block-inner td-fix-index') if content_div else ""
    all_p_tags = content_ele.find_all('p') if content_ele else ""
    data['content'] = ' '.join([p.get_text(strip = True) for p in all_p_tags])
    
    return data








def sysInit():
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = None
    try:
        print(" *************** Starting Script Hala-Canada Post Scrapping *****************\n")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # driver.maximize_window()
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

        driver.execute_script("window.scrollBy(0, 500);")
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(2)

        html = driver.page_source
        links = scrap_links(html)
        all_posts = []
        
        print(f"\n*********** All links are {len(links)} ********** \n")

        for index, link in enumerate(links) :
            print(f"Post {index+1} is scrapping")

            driver.get(link)
            time.sleep(2)
            driver.execute_script("window.scrollBy(0, 500);")
            html = driver.page_source
            
            data = scrap_data(html)
            all_posts.append(data)
        
        print("\n\n\n", json.dumps(all_posts))

        json_filename = 'all_posts_data.json'
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(all_posts, json_file, ensure_ascii=False, indent=2)

    finally:
        print("QUIT WEB DRIVER ______________")
        display.stop()
        if driver:
            driver.quit()


sysInit()