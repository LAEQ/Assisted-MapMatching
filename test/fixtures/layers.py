import os
from qgis.core import QgsVectorLayer, QgsField
from qgis.PyQt.QtCore import QVariant


class LayerFixtures:
    def __init__(self):
        self.cur_dir = os.path.dirname(__file__)

    def points_1(self):
        path = os.path.join(self.cur_dir, "points_1.geojson")
        return QgsVectorLayer(path, "points_1", "ogr")

    def points_fields_1(self):
        layer = self.points_1()
        return layer.fields()

    def points_2(self):
        path = os.path.join(self.cur_dir, "points_2.geojson")
        return QgsVectorLayer(path, os.path.basename(path), "ogr")

    def network_1(self):
        path = os.path.join(self.cur_dir, "network_1.geojson")
        return QgsVectorLayer(path, os.path.basename(path), "ogr")

    def network_2(self):
        path = os.path.join(self.cur_dir, "network_2.gpkg")
        return QgsVectorLayer(path, os.path.basename(path), "ogr")

    def points_and_networks(self):
        return [
            self.points_1(),
            self.points_2(),
            self.network_1(),
            self.network_2(),
        ]

    def generate_vector_path_4_fields(self, epsg = "4326", name = "layer_1"):
        layer = QgsVectorLayer("Point?crs=EPSG:"+epsg, name, "memory")
        pr = layer.dataProvider()  # need to create a data provider
        fields = [QgsField("id", QVariant.Int),
                  QgsField("name", QVariant.String),
                  QgsField("oid ", QVariant.Int),
                  QgsField("speed", QVariant.Double)
                  ]
        pr.addAttributes(fields)
        layer.updateFields()
        
        return layer

    # def generate_vector_path_8_fields():
    #     layer = QgsVectorLayer("Marker?crs=EPSG:4326", "layer_1", "memory")
    #     pr = layer.dataProvider()  # need to create a data provider
    #     fields = [QgsField("id", QVariant.Int),
    #               QgsField("name", QVariant.String),
    #               QgsField("oid ", QVariant.Int),
    #               QgsField("speed", QVariant.Double),
    #               QgsField("altitude", QVariant.Double),
    #               QgsField("lat", QVariant.Double),
    #               QgsField("lng", QVariant.Double),
    #               QgsField("time", QVariant.Int)
    #               ]
    #     pr.addAttributes(fields)
    #     layer.updateFields()
    #
    #     return layer
    #
    #
    def generate_network_4_fields(self,epsg = "4326", name = "layer_1"):
        layer = QgsVectorLayer("LINESTRING?crs=EPSG:"+epsg, name, "memory")
        pr = layer.dataProvider()  # need to create a data provider
        fields = [QgsField("id", QVariant.Int),
                  QgsField("name", QVariant.String),
                  QgsField("oid ", QVariant.Int),
                  QgsField("speed", QVariant.Double)
                  ]
        pr.addAttributes(fields)
        layer.updateFields()

        return layer

    def points(self):
        return [
            self.points_1(),
            self.points_2(),
        ]

    def networks(self):
        return [
            self.network_1(),
            self.network_2(),
        ]
