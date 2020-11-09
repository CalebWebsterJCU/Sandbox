"""Requests Module

import requests
request = requests.get('https://automatetheboringstuff.com/files/rj.txt')
request.raise_for_status()
print(request.status_code)
print(request.text[:500])
with open('play.txt', 'wb') as play_file:
    for chunk in request.iter_content(100000):
        play_file.write(chunk)
"""

"""Parsing HTML

import bs4
import requests
request = requests.get('https://www.pccasegear.com/products/52314/pny-geforce-rtx-3070-xlr8-epic-x-rgb-8gb')
request.raise_for_status()
soup = bs4.BeautifulSoup(request.text, 'html.parser')
name_element = soup.select('div.title > h1')
price_element = soup.select('div.price')
print(f'\nThe {name_element[0].text} costs {price_element[0].text.strip()}.')
"""

"""Selenium"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import time

# d = webdriver.Chrome(r"C:\Program Files\Chrome Driver\chromedriver.exe")
# d.get('https://techwithtim.net')
# # print(d.title)
# search = d.find_element_by_name("s")
# search.send_keys("python")
# search.send_keys(Keys.RETURN)
#
# main = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.ID, "main")))
#
# articles = main.find_elements_by_tag_name("atricle")
# for article in articles:
#     header = article.find_element_by_class_name("entry-summary")
#     print(header.text)
#
# time.sleep(5)

# link = d.find_element_by_link_text("Python Programming")
# link.click()
#
# time.sleep(3)
#
# python_link = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials")))
# python_link.click()
#
# time.sleep(3)
#
# get_started_button = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.ID, "sow-button-19310003")))
# get_started_button.click()
#
# time.sleep(3)
#
# for x in range(3):
#     d.back()
#
# time.sleep(3)
#
# for x in range(2):
#     d.forward()

# d.quit()

"""

SEARCH_TERM = "Bitspower Deluxe 1/16in Cable Sleeve - Black"
CARD_NUMBER = "5188680113972618"
EXPIRATION_DATE = "12/23"
CVV = "678"


d = webdriver.Chrome(r"C:\Program Files\Chrome Driver\chromedriver.exe")
d.get('https://pccasegear.com')
d.maximize_window()

search_bar = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.NAME, "query")))
search_bar.send_keys(SEARCH_TERM)
search_bar.send_keys(Keys.RETURN)

first_result = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, SEARCH_TERM)))
first_result.click()

title = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div.main-inner-container > div.main-content-container > div.title > h1")))
price = d.find_element_by_css_selector("#main > div.main-inner-container > div.main-content-container > div:nth-child(20) > form > div.product-desc > div.price-box > div.price")
add_to_cart = d.find_element_by_class_name("add-to-cart")
stock_label = d.find_element_by_class_name("stock-label")
info_text = d.find_element_by_id("overview")
cropped_info_text = info_text.text[:info_text.text.find('\n')]
print(f"\n{title.text}")
print(f"\n{price.text}")
print(f"\n{cropped_info_text}")
if add_to_cart.text == "ADD TO CART" or add_to_cart.text == "PRE-ORDER":
    add_to_cart.click()
    time.sleep(2)
    cart_link = d.find_element_by_class_name("cart-link")
    cart_link.click()
    checkout_button = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Checkout")))
    checkout_button.click()
    t_and_c = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.ID, "i-agree")))
    t_and_c.click()
    delivery_radio_b = d.find_element_by_id("Delivery")
    delivery_radio_b.click()
    invoice_input_ids = ["del_fname", "del_lname", "del_email", "del_telephone", "entry_saddress", "entry_street_address1", "entry_pcode"]
    invoice_details = ["Caleb", "Webster", "calebwebsteredge@gmail.com", "0400178253", "P.O Box 1350", "Tully, QLD, Australia", "4854", "TULLY"]
    for x in range(len(invoice_input_ids)):
        input_field = d.find_element_by_id(invoice_input_ids[x])
        input_field.send_keys(invoice_details[x])
        if invoice_input_ids[x] == "del_telephone":
            time.sleep(3)
            # no_signin_btn = d.find_element_by_css_selector("#checkemail_modal > div > div > div > div > form > div > button.btn.btn-light.color-black")
            no_signin_btn = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "color-black")))
            no_signin_btn.click()
    time.sleep(3)
    suburb = Select(d.find_element_by_css_selector("#delivery-billing-address > div:nth-child(7) > div.form-group.col-lg-6.col-sm-12.col-xs-12 > select"))
    suburb.select_by_visible_text(invoice_details[-1])
    delivery_input_ids = ["delivery_firstname", "delivery_lastname", "delivery_saddress", "delivery_saddress2", "delivery_pcode"]
    delivery_details = ["Caleb", "Webster", "P.O Box 1350", "Tully, QLD, Australia", "4854", "TULLY"]
    for x in range(len(delivery_input_ids)):
        input_field = d.find_element_by_id(delivery_input_ids[x])
        input_field.send_keys(delivery_details[x])
    time.sleep(3)
    suburb = Select(d.find_element_by_css_selector("#delivery-shipping-address > div:nth-child(5) > div.form-group.col-lg-6.col-sm-12.col-xs-12 > select"))
    suburb.select_by_visible_text(delivery_details[-1])
    payment_method = Select(d.find_element_by_name("payment"))
    payment_method.select_by_visible_text("Credit Card")
    card_owner = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.ID, "zzzxy-name")))
    card_owner.send_keys(f"{delivery_details[0]} {delivery_details[1]}")
    time.sleep(2)
    d.switch_to.frame("braintree-hosted-field-number")
    card_number = d.find_element_by_name("credit-card-number")
    card_number.send_keys(CARD_NUMBER)
    d.switch_to.parent_frame()
    d.switch_to.frame("braintree-hosted-field-expirationDate")
    expiration_date = d.find_element_by_name("expiration")
    expiration_date.send_keys(EXPIRATION_DATE)
    d.switch_to.parent_frame()
    d.switch_to.frame("braintree-hosted-field-cvv")
    cvv = d.find_element_by_name("cvv")
    cvv.send_keys(CVV)
    d.switch_to.parent_frame()



else:
    print("\nItem is out of stock!")
    if "/" in stock_label.text:
        print(f"Check back on {stock_label.text[5:]}")
        
"""

# d = webdriver.Chrome(r"C:\Program Files\Chrome Driver\chromedriver.exe")
# d.get('https://orteil.dashnet.org/cookieclicker/')
# # d.maximize_window()
#
# d.implicitly_wait(5)
#
# cookie = d.find_element_by_id("bigCookie")
# cookie_count = d.find_element_by_id("cookies")
# items = [d.find_element_by_id("productPrice" + str(i)) for i in range(1, -1, -1)]
#
# actions = ActionChains(d)
# actions.click(cookie)
#
# while True:
#     actions.perform()
#     count = int("".join(cookie_count.text.split(" ")[0].split(",")))
#
#     if count % 10 == 0:
#         for item in items:
#             price = int("".join(item.text.split(",")))
#             if price <= count:
#                 upgrade_actions = ActionChains(d)
#                 upgrade_actions.move_to_element(item)
#                 upgrade_actions.click()
#                 upgrade_actions.perform()


d = webdriver.Chrome(r"C:\Program Files\Chrome Driver\chromedriver.exe")
d.get('https://www.hyrtutorials.com/p/frames-practice.html')
# d.maximize_window()

# Enter text in box before switching
text_box = d.find_element(By.ID, "name")
text_box.clear()
text_box.send_keys("Before iFrame")
print(text_box.text)

# Switch to 1st iFrame
d.switch_to.frame("frm1")
d.implicitly_wait(3)
course_name = Select(d.find_element(By.ID, "course"))
course_name.select_by_visible_text("Python")

# Switch back to parent
d.switch_to.parent_frame()
text_box = d.find_element(By.ID, "name")
text_box.clear()
text_box.send_keys("After 1st iFrame")

# Switch to 2nd iFrame
d.switch_to.frame("frm2")
f_name = d.find_element(By.ID, "firstName")
f_name.clear()
f_name.send_keys("Caleb")

# Switch back to parent
d.switch_to.parent_frame()
text_box = d.find_element(By.ID, "name")
text_box.clear()
text_box.send_keys("After 2nd iFrame")

