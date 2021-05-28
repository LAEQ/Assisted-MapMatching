try:
    from .matcheur import Matcheur
except:
    print("##PLUGIN## - Couldn't load the Matcheur")

from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from qgis import processing


import string
from typing import List

class PathLayer:

    def __init__(self, _layer):
        self.initial_layer = _layer
        self.layer = None

        

    def dupplicate_initial_layer(self):
        """Copy the initial layer and create a new one with no dependances to the precedent"""
        try:
            self.initial_layer.selectAll()
            self.layer = processing.run("native:saveselectedfeatures", {'INPUT': self.initial_layer, 'OUTPUT': 'memory:'})['OUTPUT']
            self.layer.setName("Points Matché")
            self.initial_layer.removeSelection()
        except:
            return "path.dupplicate_initial_layer.processing"


    def create_buffer(self, range: int) -> QgsVectorLayer:
        """Create a buffer around every features of the path_layer.

        Input:
        range       -- The radius of the buffer around a point
        """

        if range <= 0 :
            return "path.create_buffer.buffer_range"

        # Create a list of points
        feats = [feat for feat in self.layer.getFeatures()]

        # Create a buffer around every point of the list
        buffers = [feat.geometry().buffer(range, -1).asWkt()
                   for feat in feats]

        epsg = self.layer.crs().postgisSrid()

        uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"

        # create a new layer
        mem_layer = QgsVectorLayer(uri,
                                   'buffers',
                                   'memory')

        prov = mem_layer.dataProvider()

        for i, feat in enumerate(feats):
            feat.setAttributes([i])
            feat.setGeometry(QgsGeometry.fromWkt(buffers[i]))

        prov.addFeatures(feats)

        return mem_layer


    def merge_stationary_point(self,speed_column_name: string, speed_limit : float = 0.1):
        """Merge at center every group of points which speed is lower than speed_limit.

        Input: 
        speed_column_name   -- a String which contain the name of the speed column in the selected layer
        speed_limit         -- a double which contain the max Speed where we concider that lower is a stop

        Output:
        Modify the layer of this class
        """

        #data validation
        if speed_limit < 0 :
            return "path.negative_speed_limit"

        if self.layer.fields().indexFromName(speed_column_name) == -1:
            return "path.wrong_speed_column"


        start_grouping = False

        temporary_feats = []

        for feat in self.initial_layer.getFeatures():

            if(feat[speed_column_name] <= speed_limit):
                start_grouping = True

                temporary_feats.append(feat.id())

            else:
                if(start_grouping):
                    #fusion of several points that are at a stop
                    start_grouping = False

                    self.merge_coordinate_points(temporary_feats)

                    #We empty the group and wait for the next one to form
                    temporary_feats = []


        if(start_grouping):
            self.merge_coordinate_points(temporary_feats)

        #♥QgsProject.instance().addMapLayer(self.layer)

    
    def merge_coordinate_points(self,features: List[int]):
        """Merge a list of points at their average center"""


        average_x = 0
        average_y = 0
        number_of_iteration =0

        #We calculate the average position in the group
        for feat_id in features:
            
            f = self.initial_layer.getFeature(feat_id) 

            geom = f.geometry()
            
            average_x += geom.asPoint().x()
            average_y += geom.asPoint().y()

            number_of_iteration +=1

        average_x = average_x/number_of_iteration
        average_y = average_y/number_of_iteration

        #We change the position of each point to the calculated average

        for feat_id in features:
            
            f = self.initial_layer.getFeature(feat_id) 

            #geom = f.geometry()
            geo = QgsGeometry.fromPointXY(QgsPointXY(average_x, average_y))
            self.layer.dataProvider().changeGeometryValues({ feat_id : geo })

    def speed_point_matching(self,matcheur : Matcheur, speed_column_name : string = "speed" , speed_limit : float = 1.5):
        """ Match the point in the path layer to a line by taking into account the speed
        
        Input:
        matcheur :          -- An object of class Matcheur 
        speed_column_name   -- a String which contain the name of the speed column in the selected layer
        """

        if speed_limit < 0:
            return "path.negative_speed_limit"


        if self.layer.fields().indexFromName(speed_column_name) == -1:
            return "path.wrong_speed_column"
        try:
            newpts = matcheur.snap_points_along_line(speedField = speed_column_name, speedlim= speed_limit , minpts = 5 , maxpts = float("inf"))
        except:
            return "path.speed_point_matching.matcheur.snap_points_along_line"
        if type(newpts) == str :
            return "path.speed_point_matching." + newpts

        i = 0

        for f in self.layer.getFeatures():
            geo = QgsGeometry.fromPointXY(QgsPointXY(newpts[i].x, newpts[i].y))
            self.layer.dataProvider().changeGeometryValues({ f.id() : geo })
            i += 1

        self.layer.setName("matched point by speed")

        #QgsProject.instance().addMapLayer(self.layer)

    def closest_point_matching(self, matcheur: Matcheur):
        """ Match the point in the path layer to the closest point on a line
        
        Input:
        matcheur :    -- An object of class Matcheur 
        """

        layer, error = matcheur.snap_point_to_closest()
        
        if layer == -1:
            return "path.closest_point_matching.matcheur.snap_point_to_closest.empty_layer"


        self.layer = layer

        if error != []:
            print("Warning : " + len(error) + " point were matched out of the searching radius ")
            return "path.closest_point_matching.point_out_of_range." + len(error)

        #QgsProject.instance().addMapLayer(self.layer)

    def distance_point_matching(self, matcheur: Matcheur):
        """ Match the point in the path layer to a line by taking into account the speed
        
        Input:
        matcheur :  -- An object of class Matcheur 
        """

        layer = matcheur.snap_point_by_distance()

        if layer == -1:
            return "path.distance_point_matching.matcheur.snap_point_by_distance.empty_layer"
            print("Error in matcheur.closest_point_matching")

        self.layer = layer

        #matcheur.instance().addMapLayer(self.layer)

    def reset_path(self):
        """Reselec the path used in the last matching."""
        
        self.initial_layer.selectAll()
        self.layer = processing.run("native:saveselectedfeatures", {'INPUT': self.initial_layer, 'OUTPUT': 'memory:'})['OUTPUT']
        self.layer.setName("Points Matché 2")
        self.initial_layer.removeSelection()