#!/bin/bash

ffmpeg -framerate 36.2 -f image2 -i test_create_video/imgs/000000%04d.png -tune fastdecode -movflags +faststart -c:v libx264 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -b:v:0 652k -filter:v:0 "scale=304:-1" -b:v:1 2734k -filter:v:1 "scale=912:-1" -b:v:2 9785k -filter:v:2 "scale=1824:-1" -use_timeline 1 -use_template 1 -window_size 6 -adaptation_sets "id=0,streams=v" -f dash ../../../ottometric-data/test_create_video_unit/output.mpd
