#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import argparse
import json
import shutil
import os


import google.protobuf.json_format

import op
import op_helper
import tile_png_op

class TestTilePngOp(unittest.TestCase):
    def setUp(self):
        shutil.rmtree(os.path.join(op_helper.TMP, 'in1'), ignore_errors=True)
        shutil.rmtree(os.path.join(op_helper.TMP, 'out1'), ignore_errors=True)

    def test_get_id(self):
        opp = tile_png_op.TilePngOp(op.parse_arguments(['script_success.py', 'script_version', 'user_defined_path', 'fs', json.dumps({}), 'workflow_uid', 'output_path']))
        print(opp.get_id())
        
    # def test_run(self):
    #     opp = op.Op(op.parse_arguments(['script_success.py', 'script_version', 'user_defined_path', 'fs', json.dumps({}), 'workflow_uid', 'output_path']))
    #     opp.run()

if __name__ == '__main__':
    unittest.main()

