import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": "dowlands",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True, 
        "plugins.always_open_pdf_externally": True
    })
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def search_diseases(driver, diseases):
    all_pdf_urls = {}
    for index, disease in enumerate(diseases):
        if index > 0 and index % 6 == 0:            
            driver.quit()
            time.sleep(5)
            driver = setup_driver()

        search_query = f"{disease} filetype:pdf"
        google_scholar_url = "https://scholar.google.com/"
        driver.get(google_scholar_url)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(1)
        pdf_urls = []

        for page in range(10):
            pdf_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "PDF")
            for link in pdf_links:
                href = link.get_attribute('href')
                if href not in pdf_urls:
                    pdf_urls.append(href)

            start_value = (page + 1) * 10
            next_page_url = f"https://scholar.google.com/scholar?start={start_value}&q={search_query}&hl=tr&as_sdt=0,5"
            driver.get(next_page_url)
            time.sleep(0.1)

        all_pdf_urls[disease] = pdf_urls

    return all_pdf_urls

with open('hastaliklar.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    diseases = data["Animal_disases"]

driver = setup_driver()
all_pdf_urls = search_diseases(driver, diseases)
driver.quit()
json_file_path = "all_pdf_links.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_pdf_urls, json_file, indent=4, ensure_ascii=False)

print(f"Tüm PDF linkleri JSON dosyasına kaydedildi: {json_file_path}")

 