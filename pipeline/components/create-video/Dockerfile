FROM gcr.io/valued-night-219713/bitbucket.org/ottometric-magna/data-etl_magna/base-op:9944942

RUN apt-get update -y && apt-get install -y ffmpeg

COPY ./requirements.txt /

RUN pip3 install -r /requirements.txt

COPY test_create_video /test_create_video

COPY create_video_op.py test_create_video_op.py golden_image.yaml /

RUN python3 create_video_op.py -h

RUN python3 test_create_video_op.py

COPY create_video.py test_create_video.py /

RUN python3 create_video.py -h

RUN python3 test_create_video.py

COPY integration_test_create_video_ffmpeg.py /

RUN python3 integration_test_create_video_ffmpeg.py

# RUN mkdir tmptest && python3 create_video.py test_create_video tmptest && ls tmptest && rm -rf tmptest
