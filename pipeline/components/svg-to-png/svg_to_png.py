#!/usr/bin/env python3

import os
import sys
import argparse
import base64
import cairosvg
# import cairo
# import rsvg



def main(args):
    for fileroot, _, filenames in os.walk(args.input_folder):
        for filename in filenames:
            f, e = os.path.splitext(filename)
            if e == '.svg':
                infile = os.path.join(args.input_folder, fileroot, filename)
                output = fileroot.replace(args.input_folder, args.output_folder)
                os.makedirs(output, exist_ok=True)
                outfile = os.path.join(output, f'{f}.png')

                cairosvg.svg2png(url=infile, write_to=outfile)

                # handle = rsvg.Handle(infile)
                # width, height = handle.get_dimension_data()

                # img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
                # ctx = cairo.Context(img)
                # handle.render_cairo(ctx)


                # img.write_to_png(outfile)

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str)
    parser.add_argument('output_folder', type=str)

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
