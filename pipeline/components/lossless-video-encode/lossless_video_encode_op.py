#!/usr/bin/env python3

import sys
import os
import argparse
import shutil

import op
import op_helper

import urllib

TILE_MANIFEST_JSON = 'tile_manifest.json'

SERVER = 'https://demo-dev.ottometric.com/'

class LosslessVideoEncodeOp(op.Op):
    def get_output_uri(self):
        output_uri = "%s/%s/%s/%s/" % (self.args.fs, self.driveSection.sectionId, self.args.user_defined_path, 
            self.get_id())
        print("output_uri: ", output_uri)
        return output_uri

    def get_cache_dir(self):
        return self.get_output_uri().replace('gs://', f'/mnt/fileshare/video/')

    def get_tmp_dir(self):
        return self.get_cache_dir().replace(self.get_id(), self.args.workflow_uid)

    def get_test_output_uris(self):
        return [self.get_output_uri() + 'output.webm']

    def getUIMetadata(self, metadata):
        test_output_uri = self.get_test_output_uris()[0]
        video_src = test_output_uri.replace("gs://", "https://storage.cloud.google.com/")
        demo_dev_video_src = test_output_uri.replace("gs://", f'{SERVER}video/')
        return {
            "outputs": [{
                'type': 'web-app',
                'storage': 'inline',
                'source': f'''<p><a href="{video_src}">Raw Video (bucket)</a></p>
                <p><a href="{demo_dev_video_src}">Raw Video (server)</a></p>
                <p><a href="{SERVER}video-sync/index.html?url={urllib.parse.quote(demo_dev_video_src)}">Tile Video</a></p>
                '''
            }]
        }

    def run_and_save(self, output_uri):
        tmpdir = self.get_tmp_dir()
        print(tmpdir)
        os.makedirs(tmpdir, exist_ok=True)

        (imgs_folder, timestamps_folder) = self.get_in_args()
        op_helper.observe_process(['python3', self.args.script, self.args.images_subfolder, imgs_folder, timestamps_folder, tmpdir])

        fs_tile_manifest = os.path.join(tmpdir, TILE_MANIFEST_JSON)
        tile_manifest = os.path.join(imgs_folder, TILE_MANIFEST_JSON)
        if os.path.isfile(fs_tile_manifest):
            shutil.copyfile(tile_manifest, fs_tile_manifest)

        videodir = self.get_cache_dir()
        if os.path.exists(videodir):
            shutil.rmtree(videodir)
        
        shutil.move(tmpdir, videodir)

        op_helper.observe_process(['gsutil', '-m', 'cp', '-r', f'{videodir}*', output_uri])




def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('script', type=str)
    parser.add_argument('script_version', type=str)
    parser.add_argument('user_defined_path', type=str)
    parser.add_argument('fs', type=str)
    parser.add_argument('driveSection', type=str)
    parser.add_argument('workflow_uid', type=str)
    parser.add_argument('output_path', type=str)
    parser.add_argument('images_subfolder', type=str)
    parser.add_argument('input_uris', nargs='*', type=str)

    return parser.parse_args(argv)

if __name__ == '__main__':
    opp = LosslessVideoEncodeOp(parse_arguments(sys.argv[1:]))
    opp.run()
