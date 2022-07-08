from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time

def main():
    print("starting tests...")
    path = ("chromedriver.exe")
    s = Service(path)
    driver = webdriver.Chrome(service=s)
    driver.get("https://www.demoblaze.com/")
    driver.implicitly_wait(5);
    username = "testaccout5"
    password = "testpassword5"
    signup(driver, username, password)
    add_and_delete_products_test(driver, username, password)
    input("continue?")

    
def signup(driver, username, password):
    driver.find_element(By.ID, "signin2").click()
    driver.find_element(By.ID, "sign-username").send_keys(username)
    driver.find_element(By.ID, "sign-password").send_keys(password)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(("xpath", "//button[contains(text(), 'Sign up')]"))).click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept();

def login(driver, username, password):
    driver.find_element(By.ID, "login2").click()
    driver.find_element(By.ID, "loginusername").send_keys(username)
    driver.find_element(By.ID, "loginpassword").send_keys(password)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(("xpath", "//button[contains(text(), 'Log in')]"))).click()
    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, 'logInModalLabel')))

def logout(driver):
    driver.find_element(By.ID, "logout2").click()

def add_and_delete_products_test(driver, username, password):
    login(driver, username, password)
    add_product(driver, "Samsung Galaxy s6")
    add_product(driver, "Nexus 6")
    cancel_order(driver)
    delete_product(driver)
    delete_product(driver)
    logout(driver)
    login(driver, username, password)
    assert_shopping_cart_count(driver, 0)
    add_product(driver, "Samsung Galaxy s7")
    cancel_order(driver)
    delete_product(driver)
    logout(driver)
    login(driver, username, password)
    assert_shopping_cart_count(driver, 0)

    
def assert_shopping_cart_count(driver, expected_count):
    driver.find_element("xpath", "//a[@class='nav-link'][contains(text(), 'Cart')]").click()
    cart_items = driver.find_elements("xpath", "//a[contains(text(), 'Delete')]")
    msg = "There are {count} item(s) in the shopping cart."
    assert len(cart_items) == expected_count
    print(msg.format(count=len(cart_items)))
    
def cancel_order(driver):
    driver.find_element("xpath", "//a[@class='nav-link'][contains(text(), 'Cart')]").click()
    driver.find_element("xpath", "//button[contains(text(), 'Place Order')]").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "orderModal")))
    driver.find_element(By.ID, "name").send_keys("Matthew")
    driver.find_element(By.ID, "country").send_keys("United States")
    driver.find_element(By.ID, "city").send_keys("Provo")
    driver.find_element(By.ID, "card").send_keys("1010101010101")
    driver.find_element(By.ID, "month").send_keys("April")
    driver.find_element(By.ID, "year").send_keys("2022")
    last_text_box = driver.find_element(By.ID, "year")
    ActionChains(driver)\
        .move_to_element(last_text_box)\
        .click()\
        .send_keys(Keys.TAB)\
        .send_keys(Keys.ENTER)\
        .perform()

def add_product(driver, product_name):
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(("xpath", "//a[@class='nav-link'][contains(text(), 'Home ')]"))).click()
    driver.find_element("xpath", "//a[@class='hrefch'][contains(text(), product_name)]").click()
    driver.find_element("xpath", "//a[contains(text(), 'Add to cart')]").click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept();

def delete_product(driver):
    driver.find_element("xpath", "//a[@class='nav-link'][contains(text(), 'Cart')]").click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(("xpath", "//a[contains(text(), 'Delete')]"))).click()
    time.sleep(2)

if __name__ == "__main__":
    main()
