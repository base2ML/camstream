# Standard Operating Procedures

## FFMPEG Run
ffmpeg -f video4linux2 -framerate 15 -video_size 640x480 -i /dev/video0 -vf "format=yuv420p" -c:v libx264 -preset ultrafast -tune zerolatency -f mpegts udp:192.168.1.144:77
