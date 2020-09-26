#!/usr/bin/env python3

import os
import sys
import argparse
import json

from PIL import Image

def main(args):
    pngs_by_dir = list(filter(lambda e: len(e[1]) > 0, 
        [
            (os.path.join(input_folder, fileroot), 
                list(filter(lambda t: t[1] == '.png', [os.path.splitext(filename) for filename in filenames])))
            for input_folder in args.input_folders[1::2]
            for fileroot, _, filenames in os.walk(input_folder)
        ]))

    pngs_by_frame = []
    for i in range(0, len(pngs_by_dir)):
        (dir, pngs) = pngs_by_dir[i]
        for (f, e) in pngs:
            idx = int(f)
            if len(pngs_by_frame) <= idx:
                missing = idx - len(pngs_by_frame) + 1
                while missing > 0:
                    pngs_by_frame.extend([[None] * len(pngs_by_dir)])
                    missing -= 1
            pngs_by_frame[idx][i] = os.path.join(dir, f'{f}{e}')

    (base_first_width, base_first_height) = Image.open(pngs_by_frame[0][0]).size

    os.makedirs(os.path.join(args.output_folder, 'imgs'), exist_ok=True)

    with open(os.path.join(args.output_folder, 'tile_manifest.json'), 'w') as file:
        names = [name for ids in args.input_folders[::2] for name in ids.split(",")]
        file.write(json.dumps({names[i]:
            {'x': 0, 'y': base_first_height*i, 'width': base_first_width, 'height': base_first_height}
            for i in range(0, len(names))}))

    for frame in range(0, len(pngs_by_frame)):
        im = Image.new('RGBA', (base_first_width, base_first_height*len(pngs_by_dir)), (0, 0, 0, 0))
        for i in range(0, len(pngs_by_frame[frame])):
            file = pngs_by_frame[frame][i]
            if file != None:
                im.paste(Image.open(file), (0, i*base_first_height))
        im.save(os.path.join(args.output_folder, 'imgs', f'{frame:010}.png'))

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folders', nargs='+', type=str)
    parser.add_argument('output_folder', type=str)

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
