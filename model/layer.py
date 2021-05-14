# from .pathLayer import *
# from .networkLayer import *
from qgis.core import QgsVectorLayer, QgsProject

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
        self.network_layer.select_intersection_trajectory(self.path_layer.buffer)

        
    def correct_network_layer_topology(self, close_call_tol, inter_dangle_tol):
        """Correct the topology to prevent futures error. """

        self.network_layer.correct_topology(close_call_tol, inter_dangle_tol)

    def reduce_Path_layer(self,speedRowName,speed_limit):
        """Merge stationnary point. """

        self.path_layer.merge_stationary_point(speedRowName, speed_limit)

    #=================================================================#
    #====================Matching algorithms:=========================#
    #=================================================================#

    def match_speed(self, matcheur, speed_column_name):
        """ Start the matching algorithm based on speed """

        self.network_layer.find_path(matcheur)

        self.path_layer.speed_point_matching(matcheur,speed_column_name)


    def match_closest(self,matcheur):
        """ Start the matching algorithm to the closest position on the line """

        self.network_layer.find_path(matcheur)

        self.path_layer.closest_point_matching(matcheur)


    def match_by_distance(self,matcheur):
        """ Start the matching algorithm based on the distance between each points """

        self.network_layer.find_path(matcheur)

        self.path_layer.distance_point_matching(matcheur)


    def reSelect_path(self):
        """ Select on the canvas the path used by the last matching """

        self.network_layer.select_possible_path()

    def apply_modification(self,type_of_matching,matcheur, speed_column_name = None):
        """ Change the possible path and recalculate the position of the points """

        self.network_layer.change_possible_path()
        self.path_layer.reset_path()

        network = self.network_layer.create_vector_from_path()

        matcheur.set_layers(network, self.path_layer.layer) 

        if type_of_matching == "Matching with Speed" and speed_column_name != None:
            self.path_layer.speed_point_matching(matcheur,speed_column_name)

        elif type_of_matching == "Matching closest":
            self.path_layer.closest_point_matching(matcheur)

        elif type_of_matching == "Matching by distance":
            self.path_layer.distance_point_matching(matcheur)

    def get_polyline(self):
        if self.network_layer.select_possible_path() == -1:
            return -1
        
        layer = self.network_layer.create_vector_from_path()

        layer = self.network_layer.concatenate_line(layer,"fid")

        return layer