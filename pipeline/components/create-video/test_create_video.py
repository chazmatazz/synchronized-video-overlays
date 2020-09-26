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

class MockRunProcess:
    def __init__(self, returncode, stdout):
        self.returncode = returncode
        self.stdout = stdout

class TestCreateVideo(unittest.TestCase):
    
    def setUp(self):
        outdir = os.path.join(TMP, 'test_create_video_out1')
        shutil.rmtree(outdir, ignore_errors=True)
        os.makedirs(outdir, exist_ok=True)
        with open('golden_image.yaml', 'r') as file:
            self.golden_image = yaml.safe_load(file)

    def test_getBitrate(self):
        self.assertEqual(create_video.bitrateFunction(create_video.FramerateFraction(1,1), 
            create_video.CanvasSize(1,1)), 
            1 / 7 / 1024)

    def test_getFFMpegFirstPassCommand(self):
        opp = create_video.getFFMpegFirstPassCommand(create_video.FramerateFraction(100, 3), 
                create_video.CanvasSize(1824, 942),
                os.path.join('test_create_video', 'output.webm')
            )

        
        self.assertEqual(" ".join(opp), self.golden_image['first_pass'])
        
    def test_getFFMpegCommand(self):
        opp = create_video.getFFMpegCommand(create_video.FramerateFraction(100, 3), 
                create_video.CanvasSize(1824, 942),
                os.path.join('test_create_video', 'output.webm'),
                os.path.join(TMP)
            )
        self.maxDiff = None
        self.assertEqual(" ".join(opp), self.golden_image['ffmpeg_command'])
        

    def test_getCanvasSize(self):
        self.assertEqual(create_video.getCanvasSize({"extract_frontal_camera_images": {"width":1, "height": 2}}).__dict__, create_video.CanvasSize(1,2).__dict__)

    def test_mockFramerateFraction(self):
         with patch('create_video.run_process', return_value=MockRunProcess(0, '100/3')) as mock_observe_process:
            self.assertEqual(create_video.getFramerateFraction(os.path.join('test_create_video', 'output.webm')).__dict__, create_video.FramerateFraction(100, 3).__dict__) 
            mock_observe_process.assert_called_once_with(self.golden_image['ffprobe'])

if __name__ == '__main__':
    unittest.main()

