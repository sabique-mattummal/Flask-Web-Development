  
# Import modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from random import randint


chrome_driver_path = "location"
service = Service(chrome_driver_path)
driver= webdriver.Chrome(service=service)
URL ="https://everydaypower.com/bts-quotes/"
driver.get(URL)
class Content:
    def create_quote(self):
        i = randint(23, 156)
        self.random_quote = driver.find_element(By.XPATH, f"/html/body/article/div/div/div/div[1]/p[{i}]").text
        return self.random_quote
