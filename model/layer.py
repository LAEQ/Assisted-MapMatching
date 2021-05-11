# from .pathLayer import *
# from .networkLayer import *
from qgis.core import QgsVectorLayer

class Layers:

    def __init__(self, path_layer, network_layer):
        # init classes
        self.path_layer = path_layer
        self.network_layer = network_layer

    def reduce_network_layer(self, range) -> QgsVectorLayer:
        """Makes a spatial selection on the network layer."""

        # Buffer's creation
        self.path_layer.create_buffer(range)

        # Spatial selection
        return self.network_layer.select_intersection_trajectory(self.path_layer.buffer)

        
    def correct_network_layer_topology(self, close_call_tol, inter_dangle_tol):
        """Correct the topology to prevent futures error. """

        return self.network_layer.correct_topology(close_call_tol, inter_dangle_tol)

    def reduce_Path_layer(self, speed_column_name):
        """Merge stationnary point. """

        self.path_layer.merge_stationary_point(speed_column_name)




