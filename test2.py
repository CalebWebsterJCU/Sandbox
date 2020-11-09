from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

d = webdriver.Chrome(r"C:\Program Files\Chrome Driver\chromedriver.exe")
d.get('https://the-internet.herokuapp.com/checkboxes')

checkbox = d.find_element_by_css_selector("#checkboxes > input[type=checkbox]:nth-child(1)")
checkbox.click()