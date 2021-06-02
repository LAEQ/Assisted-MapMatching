import os
import unittest
from unittest.mock import MagicMock

from qgis.core import QgsFeature, QgsPointXY

try:
    import shapely
    from shapely.geometry import LineString, Point
except:
    print("Couldn't import shapely.")

from model.utils.layerTraductor import *

from test.fixtures.layers import LayerFixtures
from test.utilities import get_qgis_app
QGIS_APP = get_qgis_app()

class TestLayerTraductor(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(__file__)
        self.fixtures = LayerFixtures()


    def test_from_vector_layer_to_list_of_dict(self):

        #normal test
        layer = self.fixtures.generate_vector_path_4_fields()
        fields = layer.fields()

        features = []
        for i in range(4):
            feat = QgsFeature(fields)
            feat.setAttributes([i, 'TEST', i, 3.14])
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(0,0)))
            features.append(feat)

        layer.dataProvider().addFeatures(features)

        res = layerTraductor.from_vector_layer_to_list_of_dict(layer)

        expected_result = [ 
            {"id" : 0 , "name" : 'TEST', "oid " : 0, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 1 , "name" : 'TEST', "oid " : 1, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 2 , "name" : 'TEST', "oid " : 2, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 3 , "name" : 'TEST', "oid " : 3, "speed": 3.14, "geometry": Point(0,0)}
            ]

        self.assertEqual(expected_result, res)

        #wrong input

        res = layerTraductor.from_vector_layer_to_list_of_dict(None)
        self.assertEqual("layer_traductor.from_vector_layer_to_list_of_dict.not_a_layer", res)


    def test_from_list_of_dict_to_layer(self):

        #normal test
        feat_list = [   
            {"id" : 0 , "name" : 'TEST', "oid " : 0, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 1 , "name" : 'TEST', "oid " : 1, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 2 , "name" : 'TEST', "oid " : 2, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 3 , "name" : 'TEST', "oid " : 3, "speed": 3.14, "geometry": Point(0,0)}
            ]
        
        

        res = layerTraductor.from_list_of_dict_to_layer(
                feat_list, 
                self.fixtures.generate_vector_path_4_fields(), 
                "Point")
        
        i = 0
        for feat in res.getFeatures():
            expected_result = [i,'TEST',i,3.14,0,0]

            geom = feat.geometry().asPoint()

            liste_result = [feat["id"], feat["name"], 
                            feat["oid "], feat["speed"], 
                            geom.x(), geom.y()]
            
            i+=1
            self.assertEqual(expected_result, liste_result)



    
    def test_order_list_of_dict(self):

        #normal test
        feat_list = [   
            {"id" : 3 , "name" : 'TEST', "oid " : 0, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 1 , "name" : 'TEST', "oid " : 1, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 2 , "name" : 'TEST', "oid " : 2, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 0 , "name" : 'TEST', "oid " : 3, "speed": 3.14, "geometry": Point(0,0)}]
        
        res = layerTraductor.order_list_of_dict(feat_list, "id")

        expected_result = [ 
            {"id" : 0 , "name" : 'TEST', "oid " : 3, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 1 , "name" : 'TEST', "oid " : 1, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 2 , "name" : 'TEST', "oid " : 2, "speed": 3.14, "geometry": Point(0,0)},
            {"id" : 3 , "name" : 'TEST', "oid " : 0, "speed": 3.14, "geometry": Point(0,0)}
            ]

        self.assertEqual(expected_result, res)

        #already sorted test
        res = layerTraductor.order_list_of_dict(feat_list, "oid ")

        self.assertEqual(feat_list,res)

        #wrong input test
        res = layerTraductor.order_list_of_dict(None, "oid ")
        self.assertEqual("layer_traductor.order_list_of_dict.error_feat_list",
                        res)

        res = layerTraductor.order_list_of_dict([], "oid ")
        self.assertEqual("layer_traductor.order_list_of_dict.error_feat_list",
                        res)

        res = layerTraductor.order_list_of_dict(feat_list, "ERROR")
        self.assertEqual("layer_traductor.order_list_of_dict.wrong_oid_column",
                        res)

        

