#!/bin/zsh
# encode.sh SRC SLUG [wide] : web copy of a film for the site (720 px wide vertical, or 1280 wide), small enough for GitHub Pages
export PATH=/opt/homebrew/bin:$PATH; cd "$(dirname "$0")"
vf="scale=720:-2"; [ "$3" = wide ] && vf="scale=1280:-2"
ffmpeg -v error -y -i "$1" -vf "$vf" -c:v libx264 -preset slow -crf 25 -maxrate 3500k -bufsize 7000k -pix_fmt yuv420p -profile:v high -c:a aac -b:a 128k -movflags +faststart video/$2.mp4 && echo "$2 $(du -h video/$2.mp4 | cut -f1)"
