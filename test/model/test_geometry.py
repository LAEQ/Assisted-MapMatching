import os
import unittest

try:
    import shapely
    from shapely.geometry import LineString, Point
except:
    print("Couldn't import shapely.")

from model.utils.geometry import *

from test.utilities import get_qgis_app
from types import SimpleNamespace
QGIS_APP = get_qgis_app()


class TestGeometry(unittest.TestCase):
    def setUp(self) -> None:
        
        self.cur_dir = os.path.dirname(__file__)



    def create_test_geometries(self):
        """build geometries, on x and y: min = 0, max = 10"""

        geometries = [  LineString([(0,0),(10,10)]),
                        LineString([(1,1),(9,9)]),
                        LineString([(2,2),(8,8)]),
                        LineString([(3,3),(7,7)]),
                        LineString([(4,4),(6,6)]),
                        LineString([(5,5),(5,5)])]
        return geometries

    def create_test_points(self):
        """build geometries, on x and y: min = 0, max = 10"""

        geometries = [  Point(0,0),
                        Point(1,1),
                        Point(2,2),
                        Point(3,3),
                        Point(4,4),
                        Point(5,5) ]
        return geometries


    def test_build_sp_index(self):

        #empty geometries
        geometries = []

        res = build_sp_index(geometries)

        self.assertEqual(None, res)

        
        geometries = self.create_test_geometries()

        res = build_sp_index(geometries)

        self.assertEqual(10,res.width)
        self.assertEqual(10,res.height)
        self.assertEqual((5,5),res.center)

    def test_nearest_geometry(self):
        geometries = self.create_test_geometries()
        index = build_sp_index(geometries)

        #closest to the geometries[0] (0,0  10,10)
        geom = LineString([(-0.5,-0.5),(10.5,10.5)])
        res = nearest_geometry(geom,index,15)
        self.assertEqual(geometries[0], res)

        #Out of range
        geom = LineString([(200,200),(201,201)])
        res = nearest_geometry(geom,index,15)
        self.assertEqual("geometry.nearest_geometry.no_candidate_found", res)

        #None values:

        res = nearest_geometry(None,index,15)
        self.assertEqual("geometry.nearest_geometry.invalid_input", res)

        res = nearest_geometry(geom,None,15)
        self.assertEqual("geometry.nearest_geometry.invalid_input", res)

        res = nearest_geometry(geom,index,0)
        self.assertEqual("geometry.nearest_geometry.invalid_input", res)

    def test_mean_point(self):

        #normal values
        points = self.create_test_points()
        res = mean_point(points, 3)
        point = Point(2.5,2.5)
        self.assertEqual(list(point.coords), list(res.coords))

        #digits = 0
        res = mean_point(points, 0)
        self.assertEqual([(2,2)], list(res.coords))

        #negative digits = same as 0
        res = mean_point(points, -3)
        self.assertEqual([(2,2)], list(res.coords))

        #empty points
        res = mean_point([], 1)
        self.assertEqual("geometry.mean_point.empty_list", res)

    
    def test_truncate(self):
        #NB: tester si nombre inexistant?

        num = truncate(3.1452,1)
        self.assertEqual(3.1,num)

        num = truncate(3.1452,0)
        self.assertEqual(3,num)

        num = truncate(3.1452,-10)
        self.assertEqual(3,num)

        num = truncate(3.1452,10)
        self.assertEqual(3.1452 ,num)


    def test_truncate_coords(self):
        #Add test on type : linestring?

        #normal case
        line = LineString([(0,0),(1,1),(3.3568,3.587), (5.32,5.235659)])

        res = truncate_coords(line, 1)
        expected_result = LineString([(0,0),(1,1),(3.3,3.5), (5.3,5.2)])
        self.assertEqual(expected_result,res)

        #0 digits
        res = truncate_coords(line, 0)
        expected_result = LineString([(0,0),(1,1),(3,3), (5,5)])
        self.assertEqual(expected_result,res)

        #negative digits
        res = truncate_coords(line, -1)
        self.assertEqual(expected_result,res)

        #line is not a LineString
        res = truncate_coords(Point(3,3), 3)
        self.assertEqual(Point(3,3),res)




    def test_truncate_coords_pts(self):
        #Add test on type : linestring?
        point = Point(3.14,12.550)

        # digits = 0
        res = truncate_coords_pts(point,0)
        expected_result = Point(3,12)
        self.assertEqual(expected_result, res)

        #negative digits
        res = truncate_coords_pts(point,-10)
        self.assertEqual(expected_result, res)

        #positive digits
        res = truncate_coords_pts(point,2)
        expected_result = Point(3.14,12.55)
        self.assertEqual(expected_result, res)

        #point is not a Point
        res = truncate_coords_pts(LineString([(3,3),(2,2)]), 3)
        self.assertEqual(LineString([(3,3),(2,2)]),res)

        
    def test_reverse_line(self):
        #je test le cas ou line = LineString()?
        #normal case
        line = LineString([(0,0),(1,1),(2,2),(3,3)])
        res = reverse_line(line)
        expected_result = LineString([(3,3),(2,2),(1,1),(0,0)])
        self.assertEqual(expected_result,res)

        """line = LineString()
        res = reverse_line(line)
        self.assertEqual("geometry.reverse_line.empty_lineString", res)
        """

    def test_get_extremites(self):

        #normal case
        line = LineString([(0,0),(1,1),(2,2),(3,3)])
        resA, resB = get_extremites(line)
        self.assertEqual( [Point(0,0),Point(3,3)] , [resA, resB] )
        
        #Not a lineString in parameter
        point = Point(2,3)
        resA, resB = get_extremites(point)
        self.assertEqual( [Point(2,3),None] , [resA, resB] )

    def test_cut_line(self):

        #Normal case attention: cut line ajoute meme en dehors
        line = LineString([ (0,0),
                            (2,2),
                            (3,3),
                            (5,5)])
        points = [  Point(1,1),
                    Point(4,4) ]
        
        res = cut_line(line,points)

        expected_result = [ LineString([(0,0),(1,1)]),
                            LineString([(1,1),(2,2),(3,3),(4,4)]),
                            LineString([(4,4),(5,5)])] 

        self.assertEqual(expected_result,res)

        #wrong input line lineString
        res = cut_line(LineString(),points)
        self.assertEqual(None,res)

        res = cut_line(None,points)
        self.assertEqual(None,res)

        res = cut_line(Point(2,3),points)
        self.assertEqual(None,res)

        #wrong point input
        res = cut_line(line,[])
        self.assertEqual([line],res)

        res = cut_line(line,None)
        self.assertEqual([line],res)

        res = cut_line(line,[LineString()])
        self.assertEqual([line],res)


    def test_cut_line_between(self):
        line = LineString([ (0,0),
                            (2,2),
                            (3,3),
                            (5,5)])

        #normal case
        p1 = Point(1,1)
        p2 = Point(4,4)

        res = cut_line_between(line,p1,p2)

        expected_result = LineString([(1,1),(2,2),(3,3),(4,4)])
        self.assertEqual(expected_result, res)

        #left is bigger
        p1 = Point(1,1)
        p2 = Point(8,8)

        res = cut_line_between(line,p1,p2)

        expected_result = LineString([(1,1),(2,2),(3,3),(5,5)])
        self.assertEqual(expected_result, res)

        #rigth is bigger
        p1 = Point(-10,-10)
        p2 = Point(2,2)

        res = cut_line_between(line,p1,p2)

        expected_result = LineString([(0,0),(2,2)])
        self.assertEqual(expected_result, res)

        #out of line (projected)

        p1 = Point(2,1)
        p2 = Point(3,2)

        res = cut_line_between(line,p1,p2)
        expected_result = LineString([(1.5,1.5),(2,2), (2.5,2.5)])
        self.assertEqual(expected_result, res)

        #wrong input
        res = cut_line_between(None,p1,p2)
        self.assertEqual(None, res)

        res = cut_line_between(LineString(),p1,p2)
        self.assertEqual(None, res)

        res = cut_line_between(line,None,p2)
        self.assertEqual([line], res)

        res = cut_line_between(line,p1,None)
        self.assertEqual([line], res)


    def test_to_simple_lines(self):

        #normal case
        line = LineString([ (0,0),
                            (2,2),
                            (3,3),
                            (5,5)])

        res = to_simple_lines(line)

        expected_result = [LineString([(0,0),(2,2)]),
                           LineString([(2,2),(3,3)]),
                           LineString([(3,3),(5,5)])]

        self.assertEqual(expected_result, res)

        #wrong input
        res = to_simple_lines(None)
        self.assertEqual([None], res)

        res = to_simple_lines(LineString())
        self.assertEqual([LineString()], res)


    def test_connect_lines(self):
        
        #verifier que les deux lignes se touchent

        #changer resultat de sortit

        #normal case
        l1 = LineString([(0,0),(1,1)])
        l2 = LineString([(1,1),(3,3)])

        res = connect_lines(l1,l2)
        expected_result = LineString([(0,0),(1,1),(3,3)])
        self.assertEqual(expected_result, res)

        ##Doen't touch each other on end
        l1 = LineString([(0,0),(1,1)])
        l2 = LineString([(2,2),(3,3)])

        res = connect_lines(l1,l2)

        
        self.assertEqual(None, res)
        
        
        #wrong input:
        res = connect_lines(None,l2)
        self.assertEqual(None, res)

        res = connect_lines(l1,None)
        self.assertEqual(None, res)
        
        
    def test_to_lixels(self):
        
        #corriger : supprimer same cote à cote

        #Normal case
        l1 = LineString([(0,0),(16,0)])
        res = to_lixels(l1,5)
        expected_result = [ LineString([(0,0),(5,0)]),
                            LineString([(5,0),(10,0)]),
                            LineString([(10,0),(15,0)]),
                            LineString([(15,0),(16,0)])]

        self.assertEqual(expected_result, res)

        #exact number
        l1 = LineString([(0,0),(15,0)])
        res = to_lixels(l1,5)
        expected_result = [ LineString([(0,0),(5,0)]),
                            LineString([(5,0),(10,0)]),
                            LineString([(10,0),(15,0)])]

        self.assertEqual(expected_result, res)

        #wrong input:
        res = to_lixels(None, 10)
        self.assertEqual(None, res)

        res = to_lixels(l1, -10)

        self.assertEqual([l1],res)



    def test_consolidate(self):
        #pbm
        
        
        points = [  Point(0,0),
                    Point(0,1),
                    Point(0,0.3),
                    Point(0,0.6),
                    Point(0,0.9),
                    Point(1,1)]

        res = consolidate(points)

        
    
    def test_splitLoop(self):

        #normal case
        loop = LineString([(0,0),(5,0),(5,5),(0,5),(0,0)])

        res = SplitLoop(loop)

        expected_result = [ LineString([(0,0),(5,0)]),
                            LineString([(5,5),(0,5),(0,0)]) ]

        self.assertEqual(expected_result, res)

        #not a splitLoop
        loop = LineString([(0,0),(5,0),(5,5),(0,5)])

        res = SplitLoop(loop)

        expected_result = [ loop ]

        self.assertEqual(expected_result, res)

        #wrong input:
        res = SplitLoop(None)
        self.assertEqual(None, res)

