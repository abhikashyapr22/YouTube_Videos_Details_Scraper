from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import time
import os
import re
import json
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

# option = Options()
# option.headless = False

option = webdriver.ChromeOptions()
option.add_argument("__headless")
driver = webdriver.Chrome(options=option)
driver.implicitly_wait(5)


def get_videos_url(go_url: str, max_links: int, interaction_time: int = 1):
    """
    :param go_url:
    :param max_links:
    :param interaction_time:
    :return:
    """

    driver.get(go_url)

    videos = driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-tab.style-scope:nth-child(4) > div:nth-child(1)')
    videos.click()

    url_list = []

    html = driver.find_element(By.TAG_NAME, 'html')

    while len(set(url_list)) < max_links:
        try:
            videos_list = driver.find_elements(By.CSS_SELECTOR, '#video-title.yt-simple-endpoint.style-scope.ytd-grid-video-renderer')
            url_list = list(dict.fromkeys(map(lambda a: a.get_attribute("href"), videos_list)))
        except:
            continue

        if len(set(url_list)) >= max_links:
            print(f"successfully scrapped {max_links} links!")
            break
        elif len(videos_list) >= max_links:
            continue
        else:
            # scroll page down
            print("working")
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(interaction_time)

    return url_list


def get_video_details(urls):
    """
    :param urls:
    :return:
    """
    # option = webdriver.ChromeOptions()
    # option.add_argument("__headless")

    vdetails = []
    for url in urls:
        """global default variables """
        title = "not found"
        videotitle = 'not found'  # for another method
        views = " not found"
        likes = "not found"
        v_img = "Not found"
        videoimage = "not found"  # for another method
        nc = "not found"

        # incase selenium did not work
        header = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

        response = requests.get(url, headers=header)
        soup1 = BeautifulSoup(response.text, "html.parser")

        # incase selenium did not work - end

        driver.get(url)
        time.sleep(3)

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
                ec.visibility_of_element_located(
                    (By.XPATH, '//*[@id="movie_player"]/div[5]/div'))).value_of_css_property(
                "background-image").split('"')[1]  # working
        except:
            print("trying another method for thumbnail")
        else:
            thumb_soup_meta = soup.find("meta", property="og:image")
            videoimage = thumb_soup_meta["content"] if thumb_soup_meta else "NotFound"

        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)

        try:
            nc = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text  # working
        except:
            print("not able to find No of comments")

        obj = dict(title=title if title else videotitle, video_link=url, views=views, likes=likes, comments=nc,
                   thumbnail=v_img if v_img else videoimage)

        vdetails.append(obj)

    return vdetails


def get_comments(url):
    title = "Not found"
    videotitle = "Not found"
    final_comment_list = []
    for url in url:
        author_list = []
        comment_list = []
        # comment_and_author_list = []

        driver.get(url)
        time.sleep(3)

        # incase selenium did not work
        header = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

        response = requests.get(url, headers=header)
        soup1 = BeautifulSoup(response.text, "html.parser")
        # incase selenium did not work - end

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            title = soup.select_one('#container h1').text  # working
        except:
            print("trying another method for title")
        else:
            title_soup_meta = soup1.find("meta", property="og:title")
            videotitle = title_soup_meta["content"] if title_soup_meta else "NotFound"

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            print("Scroll down to bottom")
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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

            obj1 = dict(title=title if title else videotitle, author_list=author_list, comment_list=comment_list)
            final_comment_list.append(obj1)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height

            # for author, comment in zip(author_list, comment_list):
            #     obj = dict(author=author, comment=comment)
            #     comment_and_author_list.append(obj)

    return final_comment_list


def save_video(folder_path: str, url: str, counter):
    """
    :param folder_path:
    :param url:
    :param counter:
    :return:
    """
    image_content = ''
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(go_url: str, target_path='./videos', number_videos: int = 1):
    """
    :param go_url:
    :param target_path:
    :param number_videos:
    :return:
    """
    target_folder = os.path.join(target_path, '_'.join("c_name"))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # with webdriver.Chrome() as driver:
    res = get_videos_url(go_url, number_videos, 2)

    counter = 0
    for elem in res:
        save_video(target_folder, elem, counter)
        counter += 1


if __name__ == "__main__":
    url = "https://www.youtube.com/user/krishnaik06"
    max_links_to_fetch = 2
    interactions_time = 3
    allVideosUrls = get_videos_url(url, max_links_to_fetch, interactions_time)
    #details = get_video_details(allVideosUrls[:max_links_to_fetch])
    commnt = get_comments(allVideosUrls[:max_links_to_fetch])
    driver.close()
    print(commnt)
