from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from qgis import processing

class PathLayer:

    def __init__(self, _layer):
        self.initial_layer = _layer

        #copy the layer and create a new one with no dependances to the precedent
        _layer.selectAll()
        self.layer = processing.run("native:saveselectedfeatures", {'INPUT': _layer, 'OUTPUT': 'memory:'})['OUTPUT']
        self.layer.setName("Points Matché")
        _layer.removeSelection()


    def create_buffer(self, range):
        """Create a buffer around every features of the path_layer.

        Input:
        range -- The radius of the buffer around a point
        """
        
        #Create a list of points
        feats = [ feat for feat in self.layer.getFeatures() ]


        #Create a buffer around every point of the list
        buffers = [ feat.geometry().buffer(range, -1).asWkt()
                    for feat in feats ]

        epsg = self.layer.crs().postgisSrid()

        uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"

        #create a new layer
        mem_layer = QgsVectorLayer(uri,
                                   'buffers',
                                   'memory')

        prov = mem_layer.dataProvider()

        for i, feat in enumerate(feats):
            feat.setAttributes([i])
            feat.setGeometry(QgsGeometry.fromWkt(buffers[i]))

        prov.addFeatures(feats)

        #ajoute à QGIS
        #QgsProject.instance().addMapLayer(mem_layer)
        self.buffer = mem_layer

    def merge_stationary_point(self,speed_row_name, precision_stop_speed = 0.1):
        """Merge at center every group of points which speed is lower than precision_stop_speed.

        Input: 
        speed_row_name       -- a String which contain the name of the speed row in the selected layer
        precision_stop_speed -- a double which contain the max Speed where we concider that lower is a stop

        Output:
        Modify the layer of this class
        """

        end_group = False

        temporary_feats = []

        for feat in self.initial_layer.getFeatures():

            if(feat[speed_row_name] <= precision_stop_speed):
                end_group = True

                temporary_feats.append(feat.id())

            else:
                if(end_group):
                    #fusion of several points that are at a stop
                    end_group = False

                    average_x = 0
                    average_y = 0
                    number_of_iteration =0

                    #We calculate the average position in the group
                    for feat_id in temporary_feats:
                        f = self.initial_layer.getFeature(feat_id +1)  #+1 because IDs start at 0 but the attribute table start at 1
                        geom = f.geometry()

                        average_x += geom.asPoint().x()
                        average_y += geom.asPoint().y()

                        number_of_iteration +=1

                    average_x = average_x/number_of_iteration
                    average_y = average_y/number_of_iteration

                    #We change the position of each point to the calculated average
                    for feat_id in temporary_feats:
                        f = self.initial_layer.getFeature(feat_id+1)  #+1 
                        geom = f.geometry()
                        geo = QgsGeometry.fromPointXY(QgsPointXY(average_x, average_y))
                        self.layer.dataProvider().changeGeometryValues({ f.id() : geo })

                    #We empty the group and wait for the next one to form
                    temporary_feats = []

            #QgsProject.instance().addMapLayer(self.layer)

    def adjust_point_on_map(self,matching):

        newpts,newdistances = matching.snap_points_along_line(speedField = "speed", speedlim=1.5 , minpts = 5 , maxpts = float("inf"))

        i = 0

        for f in self.layer.getFeatures():
            geom = f.geometry()
            geo = QgsGeometry.fromPointXY(QgsPointXY(newpts[i].x, newpts[i].y))
            self.layer.dataProvider().changeGeometryValues({ f.id() : geo })
            i += 1

        QgsProject.instance().addMapLayer(self.layer)


    def reset_path(self):
        self.initial_layer.selectAll()
        self.layer = processing.run("native:saveselectedfeatures", {'INPUT': self.initial_layer, 'OUTPUT': 'memory:'})['OUTPUT']
        self.layer.setName("Points Matché 2")
        self.initial_layer.removeSelection()

        
            
            
        



                