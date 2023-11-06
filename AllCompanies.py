from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
import time
import pandas as pd


def click_filter_es(driver):
    select_element = driver.find_element(By.ID, "field-:r6:")
    
    select = Select(select_element)
    
    select.select_by_value("ES")
    
    search_button = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div[2]/form/div[3]/button")
    search_button.click()


def extract_company_info(company_element):
    company_name = company_element.find_element(By.XPATH, ".//h5/a").text
    city_state = company_element.find_element(By.XPATH, ".//p[2]").text
    link = company_element.find_element(By.XPATH, ".//h5/a").get_attribute('href')
    return company_name, city_state, link

driver = webdriver.Chrome()

driver.get('https://certificadas.gptw.com.br/')

wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chakra-linkbox__overlay")))

click_filter_es(driver)

time.sleep(5)

company_name_list = []
city_state_list = []
link_list = []

max_page_number = int(driver.find_element(By.XPATH, '//*[@id="root"]/div[4]/div/div/button[3]').text)
for page in range(max_page_number):
    page += 1
    companies = driver.find_elements(By.XPATH, "//article")

    for company in companies:
        try:
            company_name, city_state, link = extract_company_info(company)

            company_name_list.append(company_name)
            city_state_list.append(city_state)
            link_list.append(link)
        except StaleElementReferenceException:
            companies = driver.find_elements(By.XPATH, "//article")
            continue
    next_page_button = driver.find_element(By.XPATH, f"//*[@id=\"root\"]/div[4]/div/div/button[{page}]") 

    next_page_button.click()

    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chakra-linkbox__overlay")))
    time.sleep(5)

company_info_dictionary = {"Nome da empresa": company_name_list, "Cidade/Estado": city_state_list, "Link": link_list}

company_info_dataframe = pd.DataFrame(company_info_dictionary)

company_info_dataframe = company_info_dataframe.drop_duplicates(subset= "Link")

company_info_dataframe.to_excel('companies_info_es.xlsx', index=False)

driver.quit()

