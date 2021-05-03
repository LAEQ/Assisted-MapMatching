# from .pathLayer import *
# from .networkLayer import *


class Layers:

    def __init__(self, path_layer, network_layer):
        # init classes
        self.path_layer = path_layer
        self.network_layer = network_layer

    def reduce_network_layer(self, range):
        """Makes a spatial selection on the network layer."""

        # Buffer's creation
        self.path_layer.create_buffer(range)

        # Spatial selection
        self.network_layer.select_intersection_trajectory(self.path_layer.buffer)

        print("Network layer successfuly reduced")

    def correct_network_layer_topology(self):
        """Correct the topology to prevent futures error. """

        self.network_layer.correct_topology()

    def reduce_Path_layer(self, speedRowName):
        """Merge stationnary point. """

        self.path_layer.merge_stationary_point(speedRowName)




