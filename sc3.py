import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.youtube.com/watch?v=etzmAZ7oiz0')

reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")
i=1
while not reached_page_end:
    print(f"scrolling {i}")
    driver.find_element(By.XPATH, '//body').send_keys(Keys.END)
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
        reached_page_end = True
    else:
        last_height = new_height

    i += 1
driver.quit()
