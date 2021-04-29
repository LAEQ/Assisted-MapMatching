import os
import unittest

from model.layer_manager import LayerManager
from test.fixtures.layers import LayerFixtures
from test.utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class TestLayerManager(unittest.TestCase):

    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(__file__)
        self.manager = LayerManager()
        self.fixtures = LayerFixtures()

    def test_load_filepoints_file(self):
        path = os.path.join(self.cur_dir, os.pardir, "fixtures", "points.gpkg")
        self.manager.load_layer(path)
        self.assertEqual(1, len(self.manager.layers))

    def test_set_layers(self):
        layers = self.fixtures.points_and_networks()
        self.manager.set_layers(layers)
        self.assertEqual(4, len(self.manager.layers))

    def test_add_layers(self):
        layer = self.fixtures.points_1()
        self.manager.add_layer(layer)
        layer = self.fixtures.network_1()
        self.manager.add_layer(layer)
        self.assertEqual(2, len(self.manager.layers))

    def test_is_path_layer(self):
        layer = self.fixtures.points_1()
        result = LayerManager.is_path_layer(layer)
        self.assertTrue(result)

        layer = self.fixtures.points_2()
        result = LayerManager.is_path_layer(layer)
        self.assertTrue(result)

        layer = self.fixtures.network_1()
        result = LayerManager.is_path_layer(layer)
        self.assertFalse(result)

        layer = self.fixtures.network_2()
        result = LayerManager.is_path_layer(layer)
        self.assertFalse(result)

    def test_is_network_layer(self):
        layer = self.fixtures.network_1()
        result = LayerManager.is_network_layer(layer)
        self.assertTrue(result)

        layer = self.fixtures.network_2()
        result = LayerManager.is_network_layer(layer)
        self.assertTrue(result)

        layer = self.fixtures.points_1()
        result = LayerManager.is_network_layer(layer)
        self.assertFalse(result)

        layer = self.fixtures.points_2()
        result = LayerManager.is_network_layer(layer)
        self.assertFalse(result)

    def test_path_network_layers(self):
        layers = self.fixtures.points_and_networks()
        self.manager.set_layers(layers)

        self.assertEqual(2, len(self.manager.path_layers()))
        self.assertEqual(2, len(self.manager.network_layers()))



