#!/usr/bin/env python3

import os
import sys
import argparse
import statistics
import subprocess
import bisect
import shutil
import tempfile
import json

KEYINT = 72

class FramerateFraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def getDividedFramerate(self, divisor):
        return FramerateFraction(self.numerator, self.denominator*divisor)

    def __str__(self):
        return f'{self.numerator}/{self.denominator}'

class CanvasSize:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def getDividedSize(self, divisor):
        return CanvasSize(self.width//divisor, self.height//divisor)


def bitrateFunction(framerate_fraction, canvas_size):
    # (FRAME_HEIGHT * FRAME_WIDTH * FRAME_RATE) / MOTION_FACTOR / 1024 = BASELINE Kbps
    # where MOTION_FACTOR is:

    # 7 for high-motion, high screen-change clips
    # 15 for standard clips
    # 20 for low-motion (talking head) clips

    return canvas_size.height * canvas_size.width * framerate_fraction.numerator/framerate_fraction.denominator / 7 / 1024

def getFFMpegFirstPassCommand(framerate_fraction, canvas_size, infile):
    """ pass 1 (compress) """
    print(framerate_fraction, canvas_size, infile)

    return ['ffmpeg', 
            # '-r', str(framerate_fraction),
            '-c:v', 'libvpx-vp9',
            '-i', infile, 
            '-b:v', f'{bitrateFunction(framerate_fraction, canvas_size)}k',
            '-g', str(KEYINT), '-keyint_min', str(KEYINT), '-sc_threshold', '0',
            '-c:v', 'libvpx-vp9', 
            '-pix_fmt', 'yuva420p',
            '-auto-alt-ref', '0', # needed to preserve transparency
            '-pass', '1',
            '-f', 'null', '/dev/null']

def getFFMpegCommand(framerate_fraction, canvas_size, infile, output_path):
        def getRepresentation(idx, framerate_divisor, canvas_size_divisor):
            framerate = framerate_fraction.getDividedFramerate(framerate_divisor)
            size = canvas_size.getDividedSize(canvas_size_divisor)
            bitrate_kbps = bitrateFunction(framerate, size)
            keyint = KEYINT//framerate_divisor
            return [f'-b:v:{idx}', f'{int(bitrate_kbps)}k', 
                    f'-maxrate:v:{idx}',  f'{int(bitrate_kbps*1.1)}k', 
                    f'-bufsize:v:{idx}', f'{int(bitrate_kbps*2)}k', 
                    # f'-r:v:{idx}', str(framerate), 
                    f'-g:v:{idx}', str(keyint), 
                    f'-keyint_min:v:{idx}', str(keyint), 
                    f'-filter:v:{idx}', f'"scale={size.width}:-1"']
                

        return ['ffmpeg', 
                '-c:v', 'libvpx-vp9',
                '-i', infile,
                '-movflags', '+faststart',
                '-c:v', 'libvpx-vp9',
                '-row-mt', '1',
                '-sc_threshold', '0', 
                '-map', '0:v:0', '-map', '0:a\?:0', '-map', '0:v:0', '-map', '0:a\?:0', '-map', '0:v:0', '-map', '0:a\?:0'
                ] + getRepresentation(0, 1, 4) + getRepresentation(1, 1, 2) + getRepresentation(2, 1, 1) + [
                '-use_timeline', '1', 
                '-use_template', '1', 
                '-window_size', '6', 
                '-adaptation_sets', '"id=0,streams=v"', 
                '-pix_fmt', 'yuva420p',
                '-auto-alt-ref', '0', # needed to preserve transparency
                '-f', 'dash', 
                os.path.join(output_path, 'output.mpd')]

def run_process(args, **kwargs):
    print(args)
    result = subprocess.run(args, capture_output=True, universal_newlines=True, **kwargs)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        raise Exception(result.returncode)
    return result

def getCanvasSize(tile_manifest):
    dims = tile_manifest['extract_frontal_camera_images']
    return CanvasSize(dims['width'], dims['height'])

def getFramerateFraction(video_file):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v', '-of', 'default=noprint_wrappers=1:nokey=1', '-show_entries', 'stream=r_frame_rate', video_file]
    result = run_process(cmd)
    (numerator, denominator) = result.stdout.split('/')
    return FramerateFraction(int(numerator), int(denominator))

def main(args):
    video_file = os.path.join(args.video_folder, 'output.webm')
    with open(os.path.join(args.video_folder, 'tile_manifest.json'), 'r') as file:
        canvas_size = getCanvasSize(json.load(file))
    
    framerate_fraction = getFramerateFraction(video_file)
    
    run_process(getFFMpegFirstPassCommand(framerate_fraction, canvas_size, video_file))

    run_process(" ".join(getFFMpegCommand(framerate_fraction, canvas_size, video_file, args.output_path)), shell=True)

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('video_folder', type=str)
    parser.add_argument('output_path', type=str)

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
