from qgis.core import *
from qgis import processing

class PathLayer:

    def __init__(self, _layer):
        self.initial_layer = _layer

        #copy the layer and create a new one with no dependances to the precedent
        _layer.selectAll()
        self.layer = processing.run("native:saveselectedfeatures", {'INPUT': _layer, 'OUTPUT': 'memory:'})['OUTPUT']
        _layer.removeSelection()


    def print_layer(self):
        self.move_layer()


    def move_layer(self):

        print("Start move layer")

        i = 0
        for f in self.layer.getFeatures():
                geom = f.geometry()
                geo = QgsGeometry.fromPointXY(QgsPointXY(geom.asPoint().x(), geom.asPoint().y()-10))
                self.layer.dataProvider().changeGeometryValues({ f.id() : geo })

        print("End move layer")

        #important pour afficher le changement à l'écran
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