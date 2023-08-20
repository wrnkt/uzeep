import os
import io
import subprocess
import json
import requests
import shutil
from zipfile import (
        ZipFile,
        ZIP_DEFLATED
)
from rich import print
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()

DEFAULT_FILENAME_FORMAT = "[%(uploader)s]%(title)s({}).%(ext)s"

API_KEY = os.getenv('YT_SEARCH_API_KEY')
CUR_PATH = os.path.dirname(os.path.realpath(__file__))

DOWNLOAD_PATH = os.path.join(CUR_PATH, 'download')
DL_SCRIPT = os.path.join(CUR_PATH, 'dlp.sh')

def channel_title(song_item):
    return song_item['snippet']['videoOwnerChannelTitle']


def song_item_info(song_item):
    id = song_item['snippet']['resourceId']['videoId']
    title = song_item['snippet']['title']
    return (id, title)


def channel_info(id):
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


def get_playlist_items(playlist_id):
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


def get_upload_playlist_id(channel_response):
    return channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def write_mp3s_from_channelid(channel_id):
    channel_response = channel_info('UClFmfVl1BXEhd5hw6qMGhVQ')
    playlist_id = get_upload_playlist_id(channel_response)
    items = get_playlist_items(playlist_id)

    channel_dir_path = ''
    if len(items) == 0:
        return

    title = channel_title(items[0])
    channel_dir_path = os.path.join(DOWNLOAD_PATH, title)
    os.makedirs(channel_dir_path, exist_ok=True)

    count = 1
    for song in items:
        song_id, song_title = song_item_info(song)
        print(f'songId: {song_id}')
        subprocess.run([
            DL_SCRIPT,
            song_id,
            channel_dir_path,
            DEFAULT_FILENAME_FORMAT.format(str(count))
        ])
        count += 1

    return channel_dir_path


def main():
    write_mp3s_from_channelid("dsfahsdjfhl")

if __name__ == '__main__':
    main()
