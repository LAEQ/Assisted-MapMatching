import os
from typing import List
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsField


class LayerManager:
    path_codes = [1001]
    network_codes = [1002]

    def __init__(self):
        self.layers = []
        self.selected_path = None
        self.selected_network = None

    def set_layers(self, layers: List[QgsVectorLayer]) -> None:
        self.layers = layers

    def add_layer(self, layer: QgsVectorLayer) -> None:
        self.layers.append(layer)

    def remove_layer(self, _from: int) -> None:
        del self.layers[_from]

    def path_layers(self) -> List[QgsVectorLayer]:
        return [layer for layer in self.layers if LayerManager.is_path_layer(layer)]

    def network_layers(self) -> List[QgsVectorLayer]:
        return [layer for layer in self.layers if LayerManager.is_network_layer(layer)]

    def load_layer(self, path: str) -> None:
        layer = QgsVectorLayer(path, os.path.basename(path), "ogr")
        self.layers.append(layer)

    def path_attributes(self, index: int) -> List[QgsField]:
        return self.path_layers()[index].fields()

    @classmethod
    def is_path_layer(cls, layer: QgsVectorLayer) -> bool:
        return QgsWkbTypes.flatType(layer.wkbType()) == QgsWkbTypes.Point

    @classmethod
    def is_network_layer(cls, layer: QgsVectorLayer) -> bool:
        return QgsWkbTypes.flatType(layer.wkbType()) == QgsWkbTypes.LineString

    @classmethod
    def is_valid(cls, layer: QgsVectorLayer) -> bool:
        return (cls.is_path_layer(layer) or cls.is_network_layer) and layer.isValid()
