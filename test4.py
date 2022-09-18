from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import time

"""def get_vdetails(url: str, max_links: int, interaction_time: int = 1):
    option = webdriver.ChromeOptions()
    option.add_argument("__headless")
    driver = webdriver.Chrome()

    driver.get(url)
    videos = driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-tab.style-scope:nth-child(4) > div:nth-child(1)')
    videos.click()

    url_list = []
    html = driver.find_element(By.TAG_NAME, 'html')
    while len(set(url_list)) < max_links:
        videos_list = driver.find_elements(By.CSS_SELECTOR,
                                           '#video-title.yt-simple-endpoint.style-scope.ytd-grid-video-renderer')
        url_list = list(dict.fromkeys(map(lambda a: a.get_attribute("href"), videos_list)))

        if len(set(url_list)) >= max_links:
            print(f"successfully scrapped {max_links} links!")
            driver.close()
            break
        elif len(videos_list) >= max_links:
            continue
        else:
            # scroll page down
            print("working")
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(interaction_time)

    # links = []
    # for i in range(len(elements)):
    #     links.append(elements[i].get_attribute('href'))

    vdetails = []
    for link in url_list[:max_links]:
        print('navigating to: ' + link)
        driver.get(link)

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title = soup.select_one('#container h1').text  # working
        views = driver.find_element(By.XPATH, '//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text  # working
        likes = driver.find_element(By.XPATH, '//a/yt-formatted-string[@id="text"]').text  # working
        thumbnail = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="movie_player"]/div[5]/div'))).value_of_css_property(
            "background-image").split('"')[1]  # working

        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
        nc = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text  # working

        driver.quit()

        obj = {
            'title': title,
            'views': views,
            'likes': likes,
            'comments': nc,
            'thumbnail': thumbnail
        }

        vdetails.append(obj)

    driver.back()
    return vdetails"""


def scraper(url):
    """global default variables """
    title = "not found"
    videotitle = 'not found'     # for another method
    views = " not found"
    likes = "not found"
    v_img ="Not found"
    videoimage = "not found"     # for another method

    option = webdriver.ChromeOptions()
    option.add_argument("__headless")
    driver = webdriver.Chrome()

    # incase selenium did not work
    header = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    response = requests.get(url, headers=header)
    soup1 = BeautifulSoup(response.text, "html.parser")

    # incase selenium did not work - end

    vdetails = []

    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        title = soup.select_one('#container h1').text  # working
    except:
        print("trying another method for title")
    else:
        title_soup_meta = soup1.find("meta", property="og:title")
        videotitle = title_soup_meta["content"] if title_soup_meta else "NotFound"

    try:
        views_el = driver.find_element(By.XPATH,
                                       '//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text  # working
        views = list(views_el.split())[0]
    except:
        print("Not able to extract views")

    try:
        likes = driver.find_element(By.XPATH, '//a/yt-formatted-string[@id="text"]').text  # working
    except:
        print("not able to extract likes")

    try:
        v_img = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="movie_player"]/div[5]/div'))).value_of_css_property(
            "background-image").split('"')[1]  # working
    except:
        print("trying another method for thumbnail")
    else:
        thumb_soup_meta = soup.find("meta", property="og:image")
        videoimage = thumb_soup_meta["content"] if thumb_soup_meta else "NotFound"

    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    nc = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text  # working

    driver.quit()

    obj = dict(title=title if title else videotitle, views=views, likes=likes, comments=nc,
               thumbnail=v_img if v_img else videoimage)

    vdetails.append(obj)

    return vdetails


# for author,comment in zip(author_list, comment_list[1:]):
#     print(author,': ',comment)


# for comments and author extraction
# comment_authors = driver.find_elements(By.CSS_SELECTOR,
#                                        '#author-text.yt-simple-endpoint.style-scope.ytd-comment-renderer span.style-scope.ytd-comment-renderer')
# author_list = [x.text for x in comment_authors]
#
# comments = driver.find_elements(By.CSS_SELECTOR, '#content.style-scope.ytd-expander')
# comment_list = [x.text for x in comments]


if __name__ == '__main__':
    url1 = 'https://www.youtube.com/watch?v=lkhJ7OCOCIc&t=183s'
    url = "https://www.youtube.com/user/krishnaik06"
    max_links_to_fetch = 5
    interactions_time = 3

    # res = scraper([url])
    details = scraper(url1)
    print(details)

# //*[@id="container"]/h1/yt-formatted-string
# alert = driver.switch_to.alert
# if alert:
#     driver.find_element(By.XPATH, '//button[text()="GOT IT"]').click()

# html body ytd-app div#content.style-scope.ytd-app ytd-page-manager#page-manager.style-scope.ytd-app ytd-watch-flexy.style-scope.ytd-page-manager.hide-skeleton div#columns.style-scope.ytd-watch-flexy div#primary.style-scope.ytd-watch-flexy div#primary-inner.style-scope.ytd-watch-flexy div#below.style-scope.ytd-watch-flexy ytd-comments#comments.style-scope.ytd-watch-flexy ytd-item-section-renderer#sections.style-scope.ytd-comments div#contents.style-scope.ytd-item-section-renderer ytd-comment-thread-renderer.style-scope.ytd-item-section-renderer ytd-comment-renderer#comment.style-scope.ytd-comment-thread-renderer div#body.style-scope.ytd-comment-renderer div#main.style-scope.ytd-comment-renderer div#header.style-scope.ytd-comment-renderer div#header-author.style-scope.ytd-comment-renderer h3.style-scope.ytd-comment-renderer a#author-text.yt-simple-endpoint.style-scope.ytd-comment-renderer span.style-scope.ytd-comment-renderer
# likes = soup.find('#actions div yt-formatted-string').text
# likes = driver.find_element(By.XPATH, '//*[@class="yt-simple-endpoint style-scope ytd-toggle-button-renderer"]/yt-formatted-string').get_attribute('label')
