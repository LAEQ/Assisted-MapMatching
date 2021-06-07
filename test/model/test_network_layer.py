import os
import unittest
from unittest import result
from unittest.mock import MagicMock

from model.network import NetworkLayer
from model.matcheur import Matcheur

from test.fixtures.layers import LayerFixtures
from test.utilities import get_qgis_app
QGIS_APP = get_qgis_app()

class TestNetworkLayer(unittest.TestCase):
    def setUp(self) -> None:
        
        self.cur_dir = os.path.dirname(__file__)
        self.fixtures = LayerFixtures()
        self.network_layer = NetworkLayer(self.fixtures.network_1())
    

    def test_add_attribute_to_layers(self):

        self.network_layer.layer = self.fixtures.network_1()
        result = self.network_layer.add_attribute_to_layers(None)
        self.assertEqual("network.add_attribute_to_layers.empty_attribute_name", 
                        result)


        result = self.network_layer.add_attribute_to_layers("test")

        index = self.network_layer.layer.fields().indexFromName("test")

        self.assertNotEqual(-1,index)

        i =0
        for f in self.network_layer.layer.getFeatures():
            self.assertEqual(i,f["test"])
            i+=1

        layer = self.network_layer.layer
        fields = self.network_layer.layer.fields()
        layer.dataProvider().deleteAttributes([len(fields)-1])  
        layer.updateFields()
        
    
    def test_error_find_path(self):
        self.network_layer.layer = self.fixtures.network_1()
        matcheur = Matcheur(None,None,None)

        matcheur.find_best_path_in_network = MagicMock(
                                            return_value = "graph.find.path")

        result = self.network_layer.find_path(matcheur)

        self.assertEqual("network.find_path.graph.find.path",result)
    

    def test_error_select_possible_path(self):
        self.network_layer.layer = self.fixtures.network_1()
        self.network_layer.possible_path = None

        result = self.network_layer.select_possible_path()

        self.assertEqual("network.select_possible_path.no_path_registered", 
                        result)
