import os
import unittest
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsField

from model.path import PathLayer
from test.fixtures.layers import LayerFixtures


class TestPathLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(__file__)
        self.fixtures = LayerFixtures()
        self.layer = PathLayer(self.fixtures.points_1())

    def test_create_buffer_error_negative_range(self):
        pass
        #Error: you need to activate  processing.run on qgis

        #result = self.layer.create_buffer(-1)
        #self.assertEqual(None,result)

        # self.layer.create_buffer(10)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestPathLayer)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)