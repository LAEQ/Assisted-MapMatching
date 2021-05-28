import os
import unittest
from unittest.mock import MagicMock

from qgis.core import QgsGeometry, QgsPointXY

from model.path import PathLayer
from model.matcheur import Matcheur

from test.fixtures.layers import LayerFixtures
from test.utilities import get_qgis_app
from types import SimpleNamespace
QGIS_APP = get_qgis_app()

class TestPathLayer(unittest.TestCase):
    def setUp(self) -> None:
        
        self.cur_dir = os.path.dirname(__file__)
        self.fixtures = LayerFixtures()
        self.path_layer = PathLayer(self.fixtures.points_1())

    def test_create_buffer(self):
        self.path_layer.layer = self.path_layer.initial_layer
        #range negative
        result = self.path_layer.create_buffer(-1)
        self.assertEqual("path.create_buffer.buffer_range",result)

        #range 0
        result = self.path_layer.create_buffer(0)
        self.assertEqual("path.create_buffer.buffer_range",result)

        #range normal
        result = self.path_layer.create_buffer(10)
        self.assertEqual(type(self.path_layer.initial_layer),type(result))


    def test_merge_coordinate_points(self):
        
        #attention a ne pas avoir un des fichiers de point ouvert autre part (qgis inclut)

        self.path_layer.layer = self.fixtures.points_1()
        self.path_layer.initial_layer = self.fixtures.points_1()

        geo = QgsGeometry.fromPointXY(QgsPointXY(0, 0))
        self.path_layer.initial_layer.dataProvider().changeGeometryValues({ 1 : geo })

        geo = QgsGeometry.fromPointXY(QgsPointXY(1, 0))
        self.path_layer.initial_layer.dataProvider().changeGeometryValues({ 2 : geo }) 
        
        geo = QgsGeometry.fromPointXY(QgsPointXY(0, 1))
        self.path_layer.initial_layer.dataProvider().changeGeometryValues({ 3 : geo }) 

        geo = QgsGeometry.fromPointXY(QgsPointXY(1, 1))
        self.path_layer.initial_layer.dataProvider().changeGeometryValues({ 4 : geo }) 
        
        feat_id = [1,2,3,4]

        self.path_layer.merge_coordinate_points(feat_id)

        for f in feat_id:
            f = self.path_layer.layer.getFeature(f)
            point = f.geometry().asPoint()
            pt = [point.x(),point.y()]

            self.assertEqual(pt,[0.5,0.5])


    def test_merge_stationary_point(self):
        #setup
        self.path_layer.layer = self.fixtures.points_1()

        #negative speed limit
        result = self.path_layer.merge_stationary_point("Speed", -10)
        self.assertEqual("path.negative_speed_limit", result)

        #inexisting speed column name
        result = self.path_layer.merge_stationary_point("test", 1)
        self.assertEqual("path.wrong_speed_column", result)

        #Curiously long but is working
        """
        #Test with every point matched
        self.path_layer.merge_stationary_point("Speed", 50)
        i = 0

        for point in self.path_layer.layer.getFeatures():
            if i ==0:
                pt = point.geometry().asPoint()
                i = [pt.x(),pt.y()]
            else:
                pt = point.geometry().asPoint()
                self.assertEqual(i,[pt.x(),pt.y()])
        """
        #Test with some point matched
        #We consider that 2 points aren't at the same place in our test data

        self.path_layer.layer = self.fixtures.points_1()
        self.path_layer.merge_stationary_point("Speed", 1)

        precedent_smaller_than_limit = False
        i = 0

        for point in self.path_layer.layer.getFeatures():
            pt = point.geometry().asPoint()
            if point["Speed"] <= 1:
                
                if precedent_smaller_than_limit == True:
                    self.assertEqual(i,[pt.x(),pt.y()])
                else:
                    self.assertNotEqual(i,[pt.x(),pt.y()])

                precedent_smaller_than_limit = True
            else:
                self.assertNotEqual(i,[pt.x(),pt.y()])
                precedent_smaller_than_limit = False

    def test_speed_point_matching(self):

        self.path_layer.layer = self.fixtures.points_1()
        matcheur = Matcheur(None,None,None)

        #Error from snap_point_along_line
        matcheur.snap_points_along_line = MagicMock(return_value = "test")
        result = self.path_layer.speed_point_matching(matcheur,"Speed")
        self.assertEqual("path.speed_point_matching.test",result)

        #speed limit negative
        result = self.path_layer.speed_point_matching(matcheur,speed_limit = -10)
        self.assertEqual("path.negative_speed_limit",result)

        #wrong speed_column_name
        result = self.path_layer.speed_point_matching(matcheur, 'test')
        self.assertEqual("path.wrong_speed_column",result)

        
        #normal test with list of geometry all snaped at 0,0
        list_test = []
        for f in self.path_layer.layer.getFeatures():
            list_test.append(SimpleNamespace(x=0, y =0))
        
        matcheur.snap_points_along_line = MagicMock(return_value = list_test)
        result = self.path_layer.speed_point_matching(matcheur, 'Speed', 1.5)

        self.assertEqual(result, None)
        self.assertEqual("matched point by speed", self.path_layer.layer.name())

        for f in self.path_layer.layer.getFeatures():
            pt = f.geometry().asPoint()
            self.assertEqual([0,0],[pt.x(),pt.y()])


    def test_closest_point_matching(self):
        matcheur = Matcheur(None,None,None)
        matcheur.snap_point_to_closest = MagicMock(return_value = (-1,[]))
        result = self.path_layer.closest_point_matching(matcheur)
        self.assertEqual("path.closest_point_matching.matcheur.snap_point_to_closest.empty_layer", result)


    def distance_point_matching(self):
        matcheur = Matcheur(None,None,None)
        matcheur.snap_point_by_distance = MagicMock(return_value = -1)
        result = self.path_layer.distance_point_matching(matcheur)
        self.assertEqual("distance.matching", result)


        

    
        



if __name__ == "__main__":
    suite = unittest.makeSuite(TestPathLayer)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)