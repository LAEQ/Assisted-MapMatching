import os
from typing import List
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsField, QgsProject
import string


class LayerManager:
    path_codes = [1001]
    network_codes = [1002]

    def __init__(self):
        self.layers = []
        self.selected_path = None
        self.selected_network = None

    def set_layers(self, layers: List[QgsVectorLayer]) -> None:
        self.layers = layers

    def add_layer(self, layer: QgsVectorLayer) -> None: #modif
        self.layers.append(layer)
        QgsProject.instance().addMapLayer(layer)

    def remove_layer(self, _from: int) -> None:
        try:
            del self.layers[_from]
        except Exception:
            pass

    def deselect_layer(self, name: string) ->None: #modif
        QgsProject.instance().layerTreeRoot().findLayer(self.find_layer(name).id()).setItemVisibilityChecked(False)

    def path_layers(self) -> List[QgsVectorLayer]:
        return [layer for layer in self.layers if LayerManager.is_path_layer(layer)]

    def network_layers(self) -> List[QgsVectorLayer]:
        return [layer for layer in self.layers if LayerManager.is_network_layer(layer)]

    def load_layer(self, path: str) -> None:
        layer = QgsVectorLayer(path, os.path.basename(path), "ogr")
        self.layers.append(layer)

    def path_attributes(self, index: int) -> List[QgsField]:
        try:
            return self.path_layers()[index].fields()
        except Exception:
            return []

    def find_layer(self, name: string) -> QgsVectorLayer:
        for layer in self.layers:
            if layer.name() == name:
                return layer
        return None


    @classmethod
    def is_path_layer(cls, layer: QgsVectorLayer) -> bool:
        return QgsWkbTypes.flatType(layer.wkbType()) == QgsWkbTypes.Point

    @classmethod
    def is_network_layer(cls, layer: QgsVectorLayer) -> bool:
        return QgsWkbTypes.flatType(layer.wkbType()) == QgsWkbTypes.LineString

    @classmethod
    def is_valid(cls, layer: QgsVectorLayer) -> bool:
        return (cls.is_path_layer(layer) or cls.is_network_layer) and layer.isValid()

    @classmethod
    def are_valid(cls, path: QgsVectorLayer, network: QgsVectorLayer) ->bool:
        
        if not (cls.is_valid(path) and cls.is_valid(network)):
            return False
        if network.crs().mapUnits() != 0 or path.crs().mapUnits() != 0  :
            return False
        if network.crs().authid() != path.crs().authid() :
            return False

        return True
        
