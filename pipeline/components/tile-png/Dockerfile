FROM gcr.io/valued-night-219713/bitbucket.org/ottometric-magna/data-etl_magna/base-op:9944942

COPY ./requirements.txt /

RUN pip3 install -r /requirements.txt

COPY tile_png_op.py tile_png.py /

RUN python3 tile_png_op.py -h

RUN python3 tile_png.py -h

COPY test_tile_png_op.py /

RUN python3 test_tile_png_op.py
