#!/bin/bash

ffmpeg -framerate 36.2 -f image2 -i ../../../ottometric-data/test_create_video_20/imgs/000000%04d.png -movflags +faststart -c:v libvpx-vp9 -row-mt 1 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -b:v:0 414k -filter:v:0 "scale=304:-1" -b:v:1 2607k -filter:v:1 "scale=912:-1" -b:v:2 9329k -filter:v:2 "scale=1824:-1" -use_timeline 1 -use_template 1 -window_size 6 -adaptation_sets "id=0,streams=v" -f dash ../../../ottometric-data/test_create_video_40s_TMP/output.mpd
cp ../../../ottometric-data/test_create_video_40s_TMP/output.mpd ../../../ottometric-data/test_create_video_40s/output.mpd
