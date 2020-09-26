FROM gcr.io/valued-night-219713/bitbucket.org/ottometric-magna/data-etl_magna/base-op:9944942

RUN apt-get update -y && apt-get install -y ffmpeg

COPY ./requirements.txt /

RUN pip3 install -r /requirements.txt

COPY test_create_video test_create_video/

COPY timestamps timestamps

COPY lossless_video_encode_op.py lossless_video_encode.py /

RUN python3 lossless_video_encode_op.py -h

RUN python3 lossless_video_encode.py -h

COPY test_lossless_video_encode_op.py /

RUN python3 test_lossless_video_encode_op.py

COPY test_lossless_video_encode.py golden_image.yaml /

RUN python3 test_lossless_video_encode.py

RUN mkdir tmptest && python3 lossless_video_encode.py imgs test_create_video timestamps tmptest && rm -rf tmptest
