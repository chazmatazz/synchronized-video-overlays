#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import argparse
import json
import shutil
import os
import yaml

import create_video

TMP = 'tmp'


class TestCreateVideo(unittest.TestCase):
    
    def setUp(self):
        outdir = os.path.join(TMP, 'test_create_video_out1')
        shutil.rmtree(outdir, ignore_errors=True)
        os.makedirs(outdir, exist_ok=True)
        with open('golden_image.yaml', 'r') as file:
            self.golden_image = yaml.safe_load(file)

    def test_getFFMpegFirstPassCommand(self):
        create_video.run_process(self.golden_image['first_pass'], shell=True)

    # def test_getFFMpegCommand(self): # OOM
    #     create_video.run_process(self.golden_image['ffmpeg_command'], shell=True)

    def test_getFramerateFraction(self):
        create_video.run_process(self.golden_image['ffprobe'])

if __name__ == '__main__':
    unittest.main()

