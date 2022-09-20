from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time

driver = webdriver.Chrome()
url = 'https://www.youtube.com/watch?v=etzmAZ7oiz0'

driver.get(url)
time.sleep(3)

final_comment_list = []
author_list = []
comment_list = []

last_height = driver.execute_script("return document.body.scrollHeight")
html = driver.find_element(By.TAG_NAME, 'html')
while True:
    print("Scroll down to bottom")
    # Scroll down to bottom
    html.send_keys(Keys.PAGE_DOWN)

    # Wait to load page
    time.sleep(5)

    # find author and author comment
    try:
        authors_list_el = driver.find_elements(By.CSS_SELECTOR,
                                               '#author-text.yt-simple-endpoint.style-scope.ytd-comment-renderer span.style-scope.ytd-comment-renderer')
        author_list = [x.text for x in authors_list_el]
    except:
        print(f"not able to find author for {url} video")

    try:
        comments = driver.find_elements(By.CSS_SELECTOR, '#content.style-scope.ytd-expander')
        comment_list = [x.text for x in comments]
    except:
        print(f"not able to find comments for {url} video")

    obj1 = dict(author_list=author_list, comment_list=comment_list)
    final_comment_list.append(obj1)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    else:
        last_height = new_height

print(final_comment_list)
print(len(author_list))
