from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
 
companies_info_es =  pd.read_excel(r"C:\Users\Edu\Desktop\WebScraping\companies_info_es.xlsx")

links = companies_info_es["Link"]

def extract_companies_info(driver):
    social_links_div = driver.find_element(By.CLASS_NAME, 'css-1ibau1k')

    social_links = social_links_div.find_elements(By.TAG_NAME, 'a')

    social_media_urls = [] 

    for link in social_links:
        social_media_urls.append(link.get_attribute('href'))

    company_size =  driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[1]/div/div[1]/p').text
    
    sector = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[1]/div/div[2]/p').text
    
    description = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[1]/p[2]').text
    
    igptw = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/p').text
    return social_media_urls, company_size, sector, description, igptw


driver = webdriver.Chrome()

social_media_urls_list = []
company_size_list = []
sector_list = []
description_list = []
igptw_list = []


for link in links:
    
    driver.get(link)

    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chakra-button")))
    
    social_media_urls, company_size, sector, description, igptw = extract_companies_info(driver)
    
    social_media_urls_list.append(social_media_urls)
    company_size_list.append(company_size)
    sector_list.append(sector)
    description_list.append(description)
    igptw_list.append(igptw)
    
company_info_dictionary = {"Links redes sociais": social_media_urls_list, "Tamanho da empresa": company_size_list, "Setor": sector_list, "Descrição": description_list, "IGPTW": igptw_list}

company_info_dataframe = pd.DataFrame(company_info_dictionary)

company_info_dataframe.to_excel('each_companies_info_es.xlsx', index=False)




