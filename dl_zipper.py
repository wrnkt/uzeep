import os
import io
from YTAPI import YTAPI
from Zipper import Zipper

def main():
    ytapi = YTAPI()
    channel_id = ytapi.get_channel_id("https://www.youtube.com/@prodfarside")

    zipper = Zipper()
    zip_buf, title = zipper.zip_mp3s_from_channelid(channel_id)

    if zip_buf is not None:
        with open(f'{title}.zip', 'wb') as f:
            f.write(zip_buf.getvalue())


if __name__ == '__main__':
    main()
