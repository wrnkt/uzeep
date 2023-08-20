import os
import io
from Zipper import Zipper

def main():
    zipper = Zipper()
    zip_buf, title = zipper.zip_mp3s_from_channelid('UClFmfVl1BXEhd5hw6qMGhVQ')

    if zip_buf is not None:
        with open(f'{title}.zip', 'wb') as f:
            f.write(zip_buf.getvalue())


if __name__ == '__main__':
    main()
