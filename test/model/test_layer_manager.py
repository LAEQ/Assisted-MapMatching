import os
import unittest

from model.ui.layer_manager import LayerManager
from test.fixtures.layers import LayerFixtures
from test.utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class TestLayerManager(unittest.TestCase):

    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(__file__)
        self.manager = LayerManager()
        self.fixtures = LayerFixtures()


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


    def test_remove_layer(self):
        layers = self.fixtures.points_and_networks()
        self.manager.set_layers(layers)
        self.assertEqual(4, len(self.manager.layers))

        self.manager.remove_layer(3)
        self.assertEqual(3, len(self.manager.layers))

        self.manager.remove_layer(0)
        self.assertEqual(2, len(self.manager.layers))


    def test_remove_layer_index_error(self):
        layers = self.fixtures.points_and_networks()
        self.manager.set_layers(layers)
        self.assertEqual(4, len(self.manager.layers))

        self.manager.remove_layer(4)
        self.assertEqual(4, len(self.manager.layers))


    def test_remove_layer_from_name(self):
        layers = self.fixtures.points_and_networks()

        #Empty layers
        self.manager.set_layers([])
        self.manager.remove_layer_from_name("points_2.gpkg")
        self.assertEqual(0, len(self.manager.layers))

        self.manager.set_layers(layers)

        #present value
        self.manager.remove_layer_from_name("points_2.gpkg")
        self.assertEqual(3, len(self.manager.layers))

        #non present value
        self.manager.remove_layer_from_name("TEST")
        self.assertEqual(3, len(self.manager.layers))

    def test_get_path_network_layers(self):
        layers = self.fixtures.points_and_networks()
        self.manager.set_layers(layers)

        self.assertEqual(2, len(self.manager.get_path_layers()))
        self.assertEqual(2, len(self.manager.get_network_layers()))


    def test_get_matched_layers(self):
        layers = self.fixtures.points_and_networks()
        self.manager.set_layers(layers)
        result = self.manager.get_matched_layers()
        self.assertEqual(0, len(result))

        #add a network layer with a working name
        layer =self.fixtures.generate_network_4_fields("3857","matched point by distance")
        
        self.manager.add_layer(layer)
        result = self.manager.get_matched_layers()
        self.assertEqual(0, len(result))

        #add a path layer with a working name
        layer =self.fixtures.generate_vector_path_4_fields("3857","matched point by distance")
        self.manager.add_layer(layer)
        layer =self.fixtures.generate_vector_path_4_fields("3857","matched point by speed")
        self.manager.add_layer(layer)
        layer = self.fixtures.generate_vector_path_4_fields("3857","matched point to closest")
        self.manager.add_layer(layer)
        
        result = self.manager.get_matched_layers()
        self.assertEqual(3, len(result))


    def test_get_path_attributes(self):
        layers = self.fixtures.points()
        self.manager.set_layers(layers)

        fields = self.manager.get_path_attributes(0)
        self.assertEqual(26, len(fields))
        fields = self.manager.get_path_attributes(1)
        self.assertEqual(6, len(fields))


    def test_get_path_attributes_index_out_range(self):
        fields = self.manager.get_path_attributes(1)
        self.assertEqual(0, len(fields))


    def test_load_file_points_file(self):
        path = os.path.join(self.cur_dir, os.pardir, "fixtures", "points.gpkg")
        self.manager.load_layer(path)
        self.assertEqual(1, len(self.manager.layers))


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


    def test_is_valid(self):
        layer = self.fixtures.network_1()
        result = LayerManager.is_valid(layer)
        self.assertTrue(result)

        layer = self.fixtures.generate_vector_path_4_fields()
        result = LayerManager.is_valid(layer)
        self.assertTrue(result)
    

    def test_are_valid(self):
        network = self.fixtures.network_1()
        path = self.fixtures.points_1()
        result = LayerManager.are_valid(network,path)
        self.assertTrue(result)

        path = self.fixtures.generate_vector_path_4_fields()
        result = LayerManager.are_valid(network,path)
        self.assertFalse(result)

        path = self.fixtures.generate_vector_path_4_fields("3857")
        result = LayerManager.are_valid(network,path)
        self.assertTrue(result)

        network = self.fixtures.generate_network_4_fields()
        result = LayerManager.are_valid(network,path)
        self.assertFalse(result)

        network = self.fixtures.generate_network_4_fields("3857")
        result = LayerManager.are_valid(network,path)
        self.assertTrue(result)



    

    def test_find_layer(self):
        layers = self.fixtures.points_and_networks()
        self.manager.set_layers(layers)

        #test on existing value
        layer = self.manager.find_layer("points_1.gpkg")
        self.assertEqual("points_1.gpkg",layer.name())

        #test on non existing value
        layer = self.manager.find_layer("test")
        self.assertEqual(None,layer)

    

        


if __name__ == "__main__":
    suite = unittest.makeSuite(TestLayerManager)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)