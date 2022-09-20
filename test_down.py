from pytube import YouTube


def download_video():
    a = [1,2,3,4]
    b = ['e','f','g','h']
    z = zip(a, b)
    c, d = zip(*z)

    print(c, d)
    # where to save
    # DOWNLOAD_PATH = 'https://drive.google.com/drive/folders/1rBSIFqm-7DShr2RHPdDm9YSHBthB7kH3?usp=sharing/'
    # # List of links of the video to be downloaded
    # yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
    # mp4files = yt.streams.filter(file_extension='mp4')
    # print(mp4files)
    #
    # video = yt.streams.get_by_resolution("360p")
    # title = yt.title
    # image = yt.thumbnail_url
    # print(title, image)
    # try:
    #     # downloading the video
    #     video.download(DOWNLOAD_PATH)
    # except:
    #     print("There is some Error!")
    # else:
    #     print('Videos Download Successfully!')


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=xWOoBJUqlbI"
    download_video()
