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

    def merge_stationary_point(self, speed_row_name, precision_stop_speed=0.1):
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

            if (feat[speed_row_name] <= precision_stop_speed):
                end_group = True

                temporary_feats.append(feat.id())

            else:
                if (end_group):
                    # fusion of several points that are at a stop
                    end_group = False

                    average_x = 0
                    average_y = 0
                    number_of_iteration = 0

                    # We calculate the average position in the group
                    for feat_id in feat_temp:
                        f = self.initiasl_layer.getFeature(
                            feat_id + 1)  # +1 because IDs start at 0 but the attribute table start at 1
                        geom = f.geometry()

                        average_x += geom.asPoint().x()
                        average_y += geom.asPoint().y()

                        number_of_iteration += 1

                    average_x = average_x / number_of_iteration
                    average_y = average_y / number_of_iteration

                    # We change the position of each point to the calculated average
                    for feat_id in temporary_feats:
                        f = self.initial_layer.getFeature(feat_id + 1)  # +1
                        geom = f.geometry()
                        geo = QgsGeometry.fromPointXY(QgsPointXY(average_x, average_y))
                        self.layer.dataProvider().changeGeometryValues({f.id(): geo})

                    # We empty the group and wait for the next one to form
                    temporary_feats = []

            # QgsProject.instance().addMapLayer(self.layer)

    # =========================================================================================================================
    #                                                         Perso
    # =========================================================================================================================
    def move_layer(self):

        print("Start move layer")

        i = 0
        for f in self.layer.getFeatures():
            geom = f.geometry()
            geo = QgsGeometry.fromPointXY(QgsPointXY(geom.asPoint().x(), geom.asPoint().y() - 10))
            self.layer.dataProvider().changeGeometryValues({f.id(): geo})

        print("End move layer")

        # important pour afficher le changement à l'écran
        self.layer.triggerRepaint()

    def start_point_matching():
        pass


"""
UTILE POUR APRES:
layer.selectedFeatures() : donne les points selectionné
layer.getFeatures() : renvoie tous les points
layer.selectedFeatureIds() : renvoie les ids des points selectionné

create memory layer from several points:

from qgis.core import QgsFeatureRequest

memory_layer = layer.materialize(QgsFeatureRequest().setFilterFids(layer.selectedFeatureIds()))
QgsProject.instance().addMapLayer(memory_layer)

Point de type : QgsFeature
Layer de type QGSVectorLayer

Ajoute 10 en y a tt les points du layer:
for f in self.layer.getFeatures():
    geom = f.geometry()
    geo = QgsGeometry.fromPointXY(QgsPointXY(geom.asPoint().x(), geom.asPoint().y()+10))
    self.layer.dataProvider().changeGeometryValues({ f.id() : geo })

"""