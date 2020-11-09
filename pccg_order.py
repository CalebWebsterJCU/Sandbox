import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

item_to_buy = input("What would you like to buy? ")
details = []
with open("details.txt", "r") as details_file:
    for line in details_file:
        details.append(line.strip())

f_name, l_name, email, phone, add1, add2, p_code, suburb, cc_num, exp_date, cvv = details
print(f_name, l_name, phone, add1, add2, p_code, suburb, cc_num, exp_date, cvv)

d = webdriver.Chrome(r"C:\Program Files\Chrome Driver\chromedriver.exe")
d.get('https://pccasegear.com')
d.maximize_window()

search_bar = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.NAME, "query")))
search_bar.send_keys(item_to_buy)
search_bar.send_keys(Keys.RETURN)

first_result = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, item_to_buy)))
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
if input("\nBuy this item? ") != "y":
    d.quit()
if add_to_cart.text == "ADD TO CART" or add_to_cart.text == "PRE-ORDER":
    add_to_cart.click()
    d.implicitly_wait(5)
    cart_link = d.find_element_by_class_name("cart-link")
    cart_link.click()
    checkout_button = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Checkout")))
    checkout_button.click()
    t_and_c = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.ID, "i-agree")))
    place_order = d.find_element(By.CLASS_NAME, "place_odr_btn")
    t_and_c.click()
    delivery_radio_b = d.find_element_by_id("Delivery")
    delivery_radio_b.click()
    invoice_input_ids = ["del_fname", "del_lname", "del_email", "del_telephone", "entry_saddress", "entry_street_address1", "entry_pcode"]
    invoice_details = [f_name, l_name, email, phone, add1, add2, p_code, suburb]
    for x in range(len(invoice_input_ids)):
        input_field = d.find_element_by_id(invoice_input_ids[x])
        input_field.send_keys(invoice_details[x])
    d.implicitly_wait(3)
    suburb_select = Select(d.find_element_by_css_selector("#delivery-billing-address > div:nth-child(7) > div.form-group.col-lg-6.col-sm-12.col-xs-12 > select"))
    suburb_select.select_by_visible_text(suburb)
    delivery_input_ids = ["delivery_firstname", "delivery_lastname", "delivery_saddress", "delivery_saddress2", "delivery_pcode"]
    delivery_details = [f_name, l_name, add1, add2, p_code, suburb]
    for x in range(len(delivery_input_ids)):
        input_field = d.find_element_by_id(delivery_input_ids[x])
        input_field.send_keys(delivery_details[x])
    d.implicitly_wait(3)
    suburb_select = Select(d.find_element_by_css_selector("#delivery-shipping-address > div:nth-child(5) > div.form-group.col-lg-6.col-sm-12.col-xs-12 > select"))
    suburb_select.select_by_visible_text(suburb)
    # place_order.click()
    payment_method = Select(d.find_element_by_name("payment"))
    payment_method.select_by_visible_text("Credit Card")
    card_owner = WebDriverWait(d, 10).until(EC.presence_of_element_located((By.ID, "zzzxy-name")))
    card_owner.send_keys(f"{f_name} {l_name}")
    d.implicitly_wait(3)
    d.switch_to.frame("braintree-hosted-field-number")
    card_number = d.find_element_by_name("credit-card-number")
    card_number.send_keys(cc_num)
    d.switch_to.parent_frame()
    d.switch_to.frame("braintree-hosted-field-expirationDate")
    expiration_date = d.find_element_by_name("expiration")
    expiration_date.send_keys(exp_date)
    d.switch_to.parent_frame()
    d.switch_to.frame("braintree-hosted-field-cvv")
    card_cvv = d.find_element_by_name("cvv")
    card_cvv.send_keys(cvv)
    d.switch_to.parent_frame()
    d.implicitly_wait(5)
    d.get("https://www.pccasegear.com/secure_checkout1")

else:
    print("\nItem is out of stock!")
    if "/" in stock_label.text:
        print(f"Check back on {stock_label.text[5:]}")