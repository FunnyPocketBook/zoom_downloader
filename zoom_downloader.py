import sys
import requests
import json
import logging
import re
import os
import concurrent.futures
from bs4 import BeautifulSoup
from dotmap import DotMap
with open(os.path.join(os.path.dirname(__file__), "conf.json")) as config_file:
    config = DotMap(json.load(config_file))
logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), "zoom_downloader.log"),
                    level=logging.INFO,
                    format="%(asctime)s %(message)s")

# If no arguments have been given, get the URLs from conf.json
URLS = sys.argv
if (len(URLS) > 1):
    URLS.pop(0)
else:
    URLS = config.url


def zoom_downloader(url):
    session = requests.Session() # New session for each video to keep cookies
    req = session.get(url)
    if req.status_code != 200:
        print("Error %d for %s" % (req.status_code, url))
        logging.error("Error %d for %s" % (req.status_code, url))
        return -1
    page = BeautifulSoup(req.content, "html.parser")
    topic = page.find("title").text
    video = page.find("video")
    video_request = get_video(session, video.contents[3].attrs["src"])
    save_file(topic, video_request)

# Loads whole video. This takes a while depending on your internet connection since it's actually a partial file.
def get_video(session, url):
    print("Downloading video, this may take take a while...")
    custom_headers = {
        "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
        "Referer": "https://ethz.zoom.us/",
        "Host": "ssrweb.zoom.us",
        "range": "bytes=0-"
    }
    return session.get(url, headers=custom_headers)


def save_file(fileName, request):
    name = fileName + ".mp4"
    f = open(name, "wb")
    print("Saving \"%s\" to computer..." % (name))
    for chunk in request.iter_content(chunk_size=255): 
        if chunk:
            f.write(chunk)
    print("Done.")
    f.close()


with concurrent.futures.ThreadPoolExecutor(max_workers=config.workers) as exec:
    for url in URLS:
        exec.submit(zoom_downloader, url)