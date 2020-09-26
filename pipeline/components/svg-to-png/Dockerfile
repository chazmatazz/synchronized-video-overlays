FROM gcr.io/valued-night-219713/bitbucket.org/ottometric-magna/data-etl_magna/base-op:9944942

COPY ./requirements.txt /

RUN pip3 install -r /requirements.txt

COPY svg_to_png.py /

RUN python3 svg_to_png.py -h
