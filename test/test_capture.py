# coding=utf-8
"""Tests Capture Video Tool."""


import os
import unittest
import logging
import tempfile
import shutil

from video import Capture

LOGGER = logging.getLogger('QGIS')


class TestInit(unittest.TestCase):

    capture = None

    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.file = os.path.join("..", self.cur_dir, "resources", "sample.mp4")
        self.tmp = tempfile.mkdtemp()
        self.capture = Capture(video_path=self.file, tmp_folder=self.tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def test_create_capture(self) -> None:
        result = self.capture.write(1, "mock_image.jpg")
        _, _, files = next(os.walk(self.tmp))

        self.assertTrue(result)
        self.assertEqual(1, len(files))


if __name__ == '__main__':
    unittest.main()
