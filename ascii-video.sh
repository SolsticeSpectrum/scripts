#!/bin/sh

clear

rm -f video.mp4

WHITE_COLOR='\033[1;37m'
RED_COLOR='\033[0;31m'
CYAN_COLOR='\033[0;36m'
GREEN_COLOR='\033[0;32m'

printf "${CYAN_COLOR}Enter ${RED_COLOR}You${WHITE_COLOR}Tube ${CYAN_COLOR}ID: ${GREEN_COLOR}"
read YOUTUBE_ID

clear

printf "${RED_COLOR}If throws error, try to use cookies.txt or leave empty\n"
printf "${CYAN_COLOR}Enter path to cookies.txt: ${GREEN_COLOR}"
read COOKIES

if [ "$COOKIES" = "" ]
then
   youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' http://www.youtube.com/watch?v=${YOUTUBE_ID} --output video.mp4
   mplayer -vo aa -monitorpixelaspect 0.61 -contrast -85 video.mp4
else
   youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' http://www.youtube.com/watch?v=${YOUTUBE_ID} --cookies "${COOKIES}" --output video.mp4
   mplayer -vo aa -monitorpixelaspect 0.61 -contrast -85 video.mp4
fi
