from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from qgis import processing


class PathLayer:

    def __init__(self, _layer):
        self.initial_layer = _layer

        # copy the layer and create a new one with no dependances to the precedent
        _layer.selectAll()
        self.layer = processing.run("native:saveselectedfeatures", {'INPUT': _layer, 'OUTPUT': 'memory:'})['OUTPUT']
        self.layer.setName("Points Matché")
        _layer.removeSelection()

    def create_buffer(self, range):
        """Create a buffer around every features of the path_layer.

        Input:
        range -- The radius of the buffer around a point
        """

        if range <= 0 :
            return None

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

        # ajoute à QGIS
        # QgsProject.instance().addMapLayer(mem_layer)
        self.buffer = mem_layer

    def merge_stationary_point(self,speed_column_name, speed_limit = 0.1):
        """Merge at center every group of points which speed is lower than speed_limit.

        Input: 
        speed_column_name   -- a String which contain the name of the speed column in the selected layer
        speed_limit         -- a double which contain the max Speed where we concider that lower is a stop

        Output:
        Modify the layer of this class
        """

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

        #

        if(start_grouping):
            self.merge_coordinate_points(temporary_feats)

        #♥QgsProject.instance().addMapLayer(self.layer)

    
    def merge_coordinate_points(self,features):
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

            geom = f.geometry()
            geo = QgsGeometry.fromPointXY(QgsPointXY(average_x, average_y))
            self.layer.dataProvider().changeGeometryValues({ feat_id : geo })

    def speed_point_matching(self,matcheur, speed_column_name = "speed"):
        """ Match the point in the path layer to a line by taking into account the speed
        
        Input:
        matcheur :          -- An object of class Matcheur 
        speed_column_name   -- a String which contain the name of the speed column in the selected layer
        """

        newpts = matcheur.snap_points_along_line(speedField = speed_column_name, speedlim=1.5 , minpts = 5 , maxpts = float("inf"))
        if newpts == -1:
            print("Error in matcheur.snap_points_along_line")
            return 

        i = 0

        for f in self.layer.getFeatures():
            geo = QgsGeometry.fromPointXY(QgsPointXY(newpts[i].x, newpts[i].y))
            self.layer.dataProvider().changeGeometryValues({ f.id() : geo })
            i += 1

        self.layer.setName("matched point by speed ")

        #QgsProject.instance().addMapLayer(self.layer)

    def closest_point_matching(self, matcheur):
        """ Match the point in the path layer to the closest point on a line
        
        Input:
        matcheur :    -- An object of class Matcheur 
        """

        layer = matcheur.snap_point_to_closest()

        if layer == -1:
            print("Error in matcheur.closest_point_matching")
            return

        self.layer = layer

        #QgsProject.instance().addMapLayer(self.layer)

    def distance_point_matching(self, matcheur):
        """ Match the point in the path layer to a line by taking into account the speed
        
        Input:
        matcheur :  -- An object of class Matcheur 
        """

        layer = matcheur.snap_point_by_distance()

        if layer == -1:
            print("Error in matcheur.closest_point_matching")
            return

        self.layer = layer

        #matcheur.instance().addMapLayer(self.layer)

    def reset_path(self):
        """Reselec the path used in the last matching."""
        
        self.initial_layer.selectAll()
        self.layer = processing.run("native:saveselectedfeatures", {'INPUT': self.initial_layer, 'OUTPUT': 'memory:'})['OUTPUT']
        self.layer.setName("Points Matché 2")
        self.initial_layer.removeSelection()