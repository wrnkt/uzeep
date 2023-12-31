import os
import io
import json
import requests
from zipfile import (
        ZipFile,
        ZIP_DEFLATED
)
from rich import print
from dotenv import load_dotenv
from pytube import YouTube
from urllib.request import urlopen
from bs4 import BeautifulSoup

load_dotenv()

API_KEY = os.getenv('YT_SEARCH_API_KEY')

class YTAPI:
    def __init__(self):
        pass

    def get_channel_id(self, channel_url):
        channel_page = urlopen(channel_url)
        soup = BeautifulSoup(channel_page, "lxml")
        url_tag = soup.find("meta", property="og:url")

        if url_tag:
            url = url_tag["content"]
            index = url.rfind('/')
            return url[index+1:]
        else:
            return None


    def channel_title(self, song_item):
        return song_item['snippet']['videoOwnerChannelTitle']

    def song_item_info(self, song_item):
        id = song_item['snippet']['resourceId']['videoId']
        title = song_item['snippet']['title']
        return (id, title)


    def channel_info(self, id):
        URL = 'https://www.googleapis.com/youtube/v3/channels'
        params = {
            'part': 'contentDetails',
            'maxResults': '50',
            'id': id,
            'key': API_KEY
        }
        headers = {
            'Accept': 'application/json'
        }
        return requests.get(URL, params=params, headers=headers).json()


    def get_playlist_items(self, playlist_id):
        URL = 'https://www.googleapis.com/youtube/v3/playlistItems'
        params = {
            'part': 'snippet',
            'maxResults': '50',
            'playlistId': playlist_id,
            'key': API_KEY
        }
        headers = {
            'Accept': 'application/json'
        }
        return requests.get(URL, params=params, headers=headers).json()['items']


    def get_upload_playlist_id(self, channel_response):
        return channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
