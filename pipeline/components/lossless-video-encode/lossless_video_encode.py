#!/usr/bin/env python3

import os
import sys
import argparse
import statistics
import subprocess

import dateutil.parser

def run_process(args, **kwargs):
    print(args)
    result = subprocess.run(args, capture_output=True, universal_newlines=True, **kwargs)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        raise Exception(result.returncode)
    return result

def getFramerate(mss):
    fpss = []
    for i in range(1,len(mss)):
        fps = 1/(mss[i] - mss[i-1])
        fpss.append(fps)
    
    stdev = statistics.stdev(fpss)
    mean_framerate = round(statistics.mean(fpss), 2)
    print('framerate mean: %s stdev: %s' % (mean_framerate, stdev))

    return (int(len(mss)*1e3), int((mss[-1]-mss[0])*1e3))

def getFFMpegCommand(framerate, inpattern, output_path):
    (numerator, denominator) = framerate
    return ['ffmpeg', 
        '-framerate', f'{numerator}/{denominator}', 
        '-f', 'image2', 
        '-i', inpattern, 
        '-g', '72', '-keyint_min', '72', '-sc_threshold', '0',
        '-c:v', 'libvpx-vp9', 
        '-pix_fmt', 'yuva420p',
        '-lossless', '1',
        os.path.join(output_path, 'output.webm')]

def main(args):
    mss = [] 
    with open(os.path.join(args.export_timestamps_folder, 'timestamps.txt'), 'r') as timestamps:
        line = timestamps.readline()
        while line:
            mss.append(dateutil.parser.isoparse(line.replace('\n', '')).timestamp())
            line = timestamps.readline()
    
    webm = os.path.join(args.output_path, 'output.webm')
    if os.path.exists(webm):
        os.remove(webm)
    run_process(getFFMpegCommand(getFramerate(mss), os.path.join(args.images_folder, args.images_subfolder, '000000%04d.png'), args.output_path))

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('images_subfolder', type=str)
    parser.add_argument('images_folder', type=str)
    parser.add_argument('export_timestamps_folder', type=str)
    parser.add_argument('output_path', type=str)

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
