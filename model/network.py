from qgis import processing
from qgis.core import *
from qgis.PyQt.QtCore import QVariant

# from .topology import *
from shapely import wkt

from .utils.layerTraductor import *

from .topology import *

"""
This class take care of the network layer
It has 2 objects:
It's initial layer: layer
The reduced one : reduced_layer
"""


class NetworkLayer:

    def __init__(self, _layer):
        self.initial_layer = _layer
        self.layer = self.initial_layer


    def select_intersection_trajectory(self, buffer) -> QgsVectorLayer:
        """Reduce the network layer features by only keeping the line intersecting the buffer

        Input:
        buffer -- A buffer of type QgsVectorLayer

        """

        # Sécurité: on commence à vide
        self.initial_layer.removeSelection()

        test = processing.run("qgis:selectbylocation",
                              {'INPUT': self.initial_layer, 'PREDICATE': 0, 'INTERSECT': buffer, 'METHOD': 0})

        reduced_layer = self.initial_layer.materialize(
            QgsFeatureRequest().setFilterFids(self.initial_layer.selectedFeatureIds()))
        self.initial_layer.removeSelection()

        #Deselect the precedent network
        #QgsProject.instance().layerTreeRoot().findLayer(self.initial_layer.id()).setItemVisibilityChecked(False)

        
        reduced_layer.setName("Reduced network")
        self.layer = reduced_layer

        return reduced_layer
        #QgsProject.instance().addMapLayer(self.reduced_layer)


    def correct_topology(self, close_call_tol, inter_dangle_tol):
        """Correct the topology of the layer."""

        shapely_dict = layerTraductor.from_vector_layer_to_list_of_dict(self.layer)

        # We truncate all the points value
        corrected_list = simplify_coordinates(shapely_dict, 3)

        # We split the loops  (i.e: roundabouts)
        corrected_list = cut_loops(corrected_list)

        # We take care of the intersection
        corrected_list = deal_with_danglenodes(corrected_list, inter_dangle_tol)
        corrected_list = deal_with_intersections(corrected_list, inter_dangle_tol)

        # We connect roads wich extremities are close to each other
        corrected_list = deal_with_closecall(corrected_list, close_call_tol)

        layer = layerTraductor.from_list_of_dict_to_layer(corrected_list, self.layer, "LineString", "corrected layer")

        return layer





