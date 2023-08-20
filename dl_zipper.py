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

load_dotenv()

API_KEY = os.getenv('YT_SEARCH_API_KEY')
CUR_PATH = os.path.dirname(os.path.realpath(__file__))

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


def zip_mp3s_from_channelid(channel_id):
    channel_response = channel_info('UClFmfVl1BXEhd5hw6qMGhVQ')
    playlist_id = get_upload_playlist_id(channel_response)
    items = get_playlist_items(playlist_id)

    if len(items) == 0:
        return

    title = channel_title(items[0])

    zip_buf = io.BytesIO()
    count = 1
    for song in items:
        song_id, song_title = song_item_info(song)
        print(f'songId: {song_id}')

        yt = YouTube(f"https://www.youtube.com/watch?v={song_id}")
        video = yt.streams.filter(only_audio=True).first()
        music_buf = io.BytesIO()
        video.stream_to_buffer(music_buf)

        with ZipFile(zip_buf, "a", ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr(yt.title + ".mp3", music_buf.getvalue())

        if count == 5:
            break

        count += 1

    with open(f'{title}.zip', 'wb') as f:
        f.write(zip_buf.getvalue())


def main():
    zip_mp3s_from_channelid("")

if __name__ == '__main__':
    main()
