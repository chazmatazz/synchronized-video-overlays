#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import argparse
import json
import shutil
import os


import google.protobuf.json_format

import op
import lossless_video_encode_op

TMP = 'output'

class TestLosslessVideoEncodeOp(unittest.TestCase):
    def setUp(self):
        shutil.rmtree(os.path.join(TMP, 'in1'), ignore_errors=True)
        shutil.rmtree(os.path.join(TMP, 'out1'), ignore_errors=True)

    def test_get_id(self):
        opp = lossless_video_encode_op.LosslessVideoEncodeOp(op.parse_arguments(['script_success.py', 'script_version', 'user_defined_path', 'fs', json.dumps({}), 'workflow_uid', 'output_path']))
        print(opp.get_id())
        
    # def test_run(self):
    #     opp = op.Op(op.parse_arguments(['script_success.py', 'script_version', 'user_defined_path', 'fs', json.dumps({}), 'workflow_uid', 'output_path']))
    #     opp.run()

if __name__ == '__main__':
    unittest.main()

