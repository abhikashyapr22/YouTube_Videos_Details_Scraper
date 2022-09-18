from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import time

driver = webdriver.Chrome()
url = 'https://www.youtube.com/watch?v=etzmAZ7oiz0'

driver.get(url)
wait = WebDriverWait(driver, 20)
time.sleep(3)

title = "Not found"
videotitle = "Not found"
final_comment_list = []
author_list = []
comment_list = []

last_height = driver.execute_script("return document.body.scrollHeight")
html = driver.find_element(By.TAG_NAME, 'html')

new_count = 0
old_count = 0
html.send_keys(Keys.PAGE_DOWN)
time.sleep(3)
nc = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text
while len(author_list) != int(nc):
    # old_count = new_count
    # Scroll down to bottom
    html.send_keys(Keys.PAGE_DOWN)

    # Wait to load page
    time.sleep(5)

    # find author and author comment
    try:
        authors_list_el = driver.find_elements(By.CSS_SELECTOR,
                                               '#author-text.yt-simple-endpoint.style-scope.ytd-comment-renderer span.style-scope.ytd-comment-renderer')
        author_list = [x.text for x in authors_list_el]
        new_count = len(author_list)
        print(new_count)
    except:
        print(f"not able to find author for {url} video")

    try:
        comments = driver.find_elements(By.CSS_SELECTOR, '#content.style-scope.ytd-expander')
        comment_list = [x.text for x in comments]
    except:
        print(f"not able to find comments for {url} video")

    # Calculate new scroll height and compare with last scroll height
    # new_height = driver.execute_script("return document.body.scrollHeight")
    # if old_count == new_count:
    #     break





# while True:
#     old_count = new_count
#     html.send_keys(Keys.PAGE_DOWN)
#     #list_com = wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, '#author-text.yt-simple-endpoint.style-scope.ytd-comment-renderer span.style-scope.ytd-comment-renderer'))
#     list_com = driver.find_elements(By.CSS_SELECTOR, '#author-text.yt-simple-endpoint.style-scope.ytd-comment-renderer span.style-scope.ytd-comment-renderer')
#     new_count = len(list_com)
#     print(new_count)
#
#     # scroll down to last product to trigger the loading spinner
#     # driver.execute_script("arguments[0].scrollIntoView();", list_com[len(list_com) - 1])
#     # html.send_keys(Keys.PAGE_DOWN)
#
#     # wait for loading spinner to appear and then disappear
#     # wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.infinite-scroll-loader")))
#     # wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, "div.infinite-scroll-loader")))
#
#     # if the count didn't change, we've loaded all products on the page
#     # I put a max of 50 products to load as a demo. You can adjust higher as needed but you should put something reasonably sized here to prevent the script from running for an hour
#     if new_count == old_count:   #  or new_count > 50
#         break
