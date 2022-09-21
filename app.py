from flask import Flask, render_template, redirect, url_for, request, flash, send_file, session, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from pytube import YouTube
from flask_pymongo import PyMongo
import pandas as pd
import logging
from io import BytesIO
import pymongo
import time
import os
import re
import json
import requests

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

option = webdriver.ChromeOptions()
option.add_argument("__headless")

# configuring database for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_details.sqlite3'

db = SQLAlchemy(app)
app.secret_key = 'tdyduytie567658trfgbhfgbxr67hftgbh'


# creating database
class VideoDetails(db.Model):
    id = db.Column('VideoDetails', db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    url = db.Column(db.String(500))
    views = db.Column(db.String(50))
    likes = db.Column(db.String(50))
    comments = db.Column(db.String(50))
    thumbnail = db.Column(db.String(100))

    def __init__(self, title, url, views, likes, comments, thumbnail):
        self.title = title
        self.url = url
        self.views = views
        self.likes = likes
        self.comments = comments
        self.thumbnail = thumbnail


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

def get_videos_url(driver, go_url: str, max_links: int, interaction_time: int = 1):
    logging.basicConfig(filename="scraper_app.log", level=logging.INFO,
                        format='%(levelname)s %(asctime)s %(name)s %(message)s')
    """
    :param go_url:
    :param max_links:
    :param interaction_time:
    :return:
    """
    print(f"found url {go_url}")
    driver.get(go_url)

    try:
        videos = driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-tab.style-scope:nth-child(4) > div:nth-child(1)')
        videos.click()
    except:
        return ''

    url_list = []

    html = driver.find_element(By.TAG_NAME, 'html')

    while len(set(url_list)) < max_links:
        try:
            videos_list = driver.find_elements(By.CSS_SELECTOR,
                                               '#video-title.yt-simple-endpoint.style-scope.ytd-grid-video-renderer')
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

    return url_list[:max_links]


@app.route('/get_video_details/', methods=['POST', 'GET'])
def get_video_details():
    if request.method == 'POST':
        ch_link = str(request.form['url'])
        max_links = 1
        interaction_time = 1
        driver = webdriver.Chrome(options=option)
        # driver.implicitly_wait(5)

        urls = get_videos_url(driver, ch_link, max_links, interaction_time)

        if urls == 'None':
            flash("Something went wrong! Please refresh the page or try with different url")
            return redirect(url_for('/'))

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

            # Using YouTube api at last
            yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)

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
                title_soup_meta = soup1.find("meta", property="og:title")
                videotitle = title_soup_meta["content"] if title_soup_meta else "Not Found"
                if not videotitle:
                    title = yt.title if yt.title else "Not Found"
            else:
                print("title found")

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
                thumb_soup_meta = soup.find("meta", property="og:image")
                videoimage = thumb_soup_meta["content"] if thumb_soup_meta else "Not Found"
                if not videoimage:
                    v_img = yt.thumbnail_url if yt.thumbnail_url else "Not Found"
            else:
                print("thumbnail found")

            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)

            try:
                nc = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text  # working
            except:
                print("not able to find No of comments")

            # obj = dict(title=title if title else videotitle, url=url, views=views, likes=likes, comments=nc,
            #            thumbnail=v_img if v_img else videoimage)

            #vdetails.append(obj)

            insert_data = VideoDetails(title=title if title else videotitle, url=url, views=views, likes=likes, comments=nc, thumbnail=v_img if v_img else videoimage)
            db.session.add(insert_data)
            db.session.commit()

        print(VideoDetails.query.all())
        return render_template('result_test.html', vdata=VideoDetails.query.all())

    else:
        return render_template('result_test.html', vdata=VideoDetails.query.all())


@app.route('/download', methods=["POST", "GET"])
def download_video():
    if request.method == "POST":
        buffer = BytesIO()
        # quality = request.form['quality']
        url = request.form['url']
        title = request.form['title']

        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        mp4files = yt.streams.filter(file_extension='mp4')
        quality = "Medium"

        if "360p" in [i.resolution for i in mp4files]:
            video = yt.streams.get_by_resolution("360p")
        elif "480p" in [i.resolution for i in mp4files]:
            video = yt.streams.get_by_resolution("480p")
        else:
            video = yt.streams.get_by_resolution("720p")

        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=title+'.mp4', mimetype='video/mp4')

    return render_template('result_test.html', vdata=VideoDetails.query.all())


@app.route('/comments', methods=['POST', 'GET'])
def get_comments():
    if request.method == "POST":
        url = request.form['url']
        driver = webdriver.Chrome()

        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        v_id = yt.video_id

        driver.get(url)
        time.sleep(3)

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

            # obj1 = dict(author_list=author_list, comment_list=comment_list)
            # final_comment_list.append(obj1)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                last_height = new_height

        data = {
            "Name": author_list,
            "Comment": comment_list
        }
        df = pd.DataFrame(data)

        try:
            mongo.save_file("comments.csv", df.to_csv())
            mongo.send_file("comments.csv")
            print("Done!")
        except:
            print("Check your connection")

        return render_template('comment.html', data=zip(author_list, comment_list))

    else:
        return render_template('result_test.html', vdata=VideoDetails.query.all())

@app.route('/save', methods=['POST', 'GET'])
def save_comments():
    if request.method == 'POST':
        data = request.form['data']
        formt = request.form['format']

        print(data)

        # saving the comment file
        target_folder = '/static/downloads'
        os.makedirs(target_folder, exist_ok=True)
        # if not os.path.exists(target_folder):
        #     os.makedirs(target_folder)
        # names, comments = zip(*data)
        # df = pd.DataFrame({"Name": names, "comment": comments}, columns=['Name', 'Comment'])
        # if formt == 'csv':
        #     df.to_csv(target_folder+'/comments.csv')
        # else:
        #     df.to_excel(target_folder+'/comments.xlsx')
        return render_template('result_test.html', vdata=VideoDetails.query.all())
    else:
        return render_template('result_test.html', vdata=VideoDetails.query.all())

if __name__ == '__main__':
    app.run(debug=True, port=5002)
