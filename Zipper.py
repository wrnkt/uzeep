import io
from pytube import YouTube
from zipfile import (
        ZipFile,
        ZIP_DEFLATED
)
from YTAPI import YTAPI

class Zipper:
    def __init__(self):
        pass

    def zip_mp3s_from_channelid(self, channel_id):
        ytapi = YTAPI()
        channel_response = ytapi.channel_info(channel_id)
        playlist_id = ytapi.get_upload_playlist_id(channel_response)
        items = ytapi.get_playlist_items(playlist_id)

        if len(items) == 0:
            return None, None

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
                zip_file.writestr(yt.title + f" ({count}) " + ".mp3", music_buf.getvalue())

            count += 1

        return zip_buf, title
