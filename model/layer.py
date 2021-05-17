from .matcheur import Matcheur
import string
from .path import PathLayer
from .network import NetworkLayer
from qgis.core import QgsVectorLayer, QgsProject, QgsFeature
from .utils.layerTraductor import *

class Layers:

    def __init__(self, path_layer : PathLayer, network_layer : NetworkLayer):
        # init classes
        self.path_layer = path_layer
        self.network_layer = network_layer

    def reduce_network_layer(self, range: int) -> None:
        """Makes a spatial selection on the network layer."""

        # Buffer's creation
        self.path_layer.create_buffer(range)

        # Spatial selection
        self.network_layer.select_intersection_trajectory(self.path_layer.buffer)

        
    def correct_network_layer_topology( self, close_call_tol : float, 
                                        inter_dangle_tol : float):
        """Correct the topology to prevent futures error. """

        self.network_layer.correct_topology(close_call_tol, inter_dangle_tol)


    def reduce_path_layer(self,speed_column_name: string,speed_limit : float):
        """Merge stationnary point. """

        self.path_layer.merge_stationary_point(speed_column_name, speed_limit)

    #=================================================================#
    #====================Matching algorithms:=========================#
    #=================================================================#

    def match_speed(self, matcheur : Matcheur, 
                    speed_column_name : string) -> None:
        """ Start the matching algorithm based on speed """

        self.network_layer.find_path(matcheur)

        self.path_layer.speed_point_matching(matcheur,speed_column_name)

        self.polyline = matcheur.polyline


    def match_closest(self,matcheur : Matcheur):
        """ Start the matching algorithm to the closest position on the line """

        self.network_layer.find_path(matcheur)

        self.path_layer.closest_point_matching(matcheur)

        self.polyline = matcheur.polyline


    def match_by_distance(self,matcheur : Matcheur):
        """ Start the matching algorithm based on the distance between each points """

        self.network_layer.find_path(matcheur)

        self.path_layer.distance_point_matching(matcheur)

        self.polyline = matcheur.polyline


    def reSelect_path(self):
        """ Select on the canvas the path used by the last matching """

        self.network_layer.select_possible_path()

    def apply_modification( self,type_of_matching : string,
                            matcheur : Matcheur, 
                            speed_column_name : string = None):
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

        self.polyline = matcheur.polyline

    def get_polyline(self):
        """ Return a QgsVectorLayer created from a single Linestring : 
            the last polyline created by the matching algorithm
            """

        epsg = self.network_layer.layer.crs().postgisSrid()

        typ = "Linestring?crs=EPSG:"+ str(epsg)

        mem_layer = QgsVectorLayer(typ,"polyline","memory")

        temp = [{"geometry" : self.polyline}]

        mem_layer = layerTraductor.from_list_of_dict_to_layer(temp,mem_layer)

        return mem_layer