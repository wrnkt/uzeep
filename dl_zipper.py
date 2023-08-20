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
from YTAPI import YTAPI

load_dotenv()

def zip_mp3s_from_channelid(channel_id):
    ytapi = YTAPI()
    channel_response = ytapi.channel_info(channel_id)
    playlist_id = ytapi.get_upload_playlist_id(channel_response)
    items = ytapi.get_playlist_items(playlist_id)

    if len(items) == 0:
        return NULL

    title = ytapi.channel_title(items[0])

    zip_buf = io.BytesIO()
    count = 1
    for song in items:
        song_id, song_title = ytapi.song_item_info(song)
        print(f'songId: {song_id}')

        yt = YouTube(f"https://www.youtube.com/watch?v={song_id}")
        video = yt.streams.filter(only_audio=True).first()
        music_buf = io.BytesIO()
        video.stream_to_buffer(music_buf)

        with ZipFile(zip_buf, "a", ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr(yt.title + ".mp3", music_buf.getvalue())

        count += 1

    return zip_buf


def main():
    zip_buf = zip_mp3s_from_channelid('UClFmfVl1BXEhd5hw6qMGhVQ')

    if zip_buf is not NULL:
        with open(f'{title}.zip', 'wb') as f:
            f.write(zip_buf.getvalue())


if __name__ == '__main__':
    main()
