#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import argparse
import json
import shutil
import os
import yaml

import lossless_video_encode

TMP = 'output'

class TestLosslessVideoEncode(unittest.TestCase):
    
    def setUp(self):
        outdir = os.path.join(TMP, 'test_create_video_out1')
        shutil.rmtree(outdir, ignore_errors=True)
        os.makedirs(outdir, exist_ok=True)

        with open('golden_image.yaml', 'r') as file:
            self.golden_image = yaml.safe_load(file)

    def test_getFramerate(self):
        self.assertEqual(lossless_video_encode.getFramerate([2,4,5,10]), (4*1e3,8*1e3))

    def test_getFFMpegCommand(self):
        opp = lossless_video_encode.getFFMpegCommand((100, 3), 
                os.path.join('test_create_video', 'imgs', '000000%4d.png'),
                os.path.join(TMP, 'test_create_video_out1')
            )

        self.maxDiff = None
        self.assertEqual(" ".join(opp), self.golden_image['base_encode'])
        

if __name__ == '__main__':
    unittest.main()

