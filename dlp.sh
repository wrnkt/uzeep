#!/bin/bash

url="https://www.youtube.com/watch?v=$1"
#yt-dlp -f 'ba' -x --audio-format mp3 $url -o "$2/[%(uploader)s]%(title)s($3).%(ext)s"
yt-dlp -f 'ba' -x --audio-format mp3 $url -o "$2/[%(uploader)s]%(title)s($3).%(ext)s"
