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
        buffer = self.path_layer.create_buffer(range)

        if type(buffer) == str:
            return "layer.reduce_network_layer." + buffer

        # Spatial selection
        error = self.network_layer.select_intersection_trajectory(buffer)
        if error != None:
            return "layer.reduce_network_layer." + error


        
    def correct_network_layer_topology( self, close_call_tol : float, 
                                        inter_dangle_tol : float):
        """Correct the topology to prevent futures error. """

        error = self.network_layer.correct_topology(close_call_tol, inter_dangle_tol)

        if error != None:
            return "layer.correct_network_layer_topology." + error

    def reduce_path_layer(self,speed_column_name: string,speed_limit : float):
        """Merge stationnary point. """

        error = self.path_layer.merge_stationary_point(speed_column_name, speed_limit)

        if error != None:
            return "layer.reduce_path_layer." + error

    #=================================================================#
    #====================Matching algorithms:=========================#
    #=================================================================#

    def match_speed(self, matcheur : Matcheur, 
                    speed_column_name : string,
                    speed_lim: float) -> None:
        """ Start the matching algorithm based on speed """

        error = self.reduce_path_layer(speed_column_name, speed_lim)

        if error != None:
            return error

        error = self.network_layer.find_path(matcheur)

        if error != None:
            return "layer.match_speed."+ error

        error = self.path_layer.speed_point_matching(matcheur,speed_column_name, speed_limit= speed_lim)

        if error != None:
            return "layer.match_speed."+ error

        self.polyline = matcheur.polyline


    def match_closest(self,matcheur : Matcheur):
        """ Start the matching algorithm to the closest position on the line """

        self.network_layer.find_path(matcheur)

        res = self.path_layer.closest_point_matching(matcheur)

        self.polyline = matcheur.polyline


    def match_by_distance(self,matcheur : Matcheur):
        """ Start the matching algorithm based on the distance between each points """

        self.network_layer.find_path(matcheur)

        self.path_layer.distance_point_matching(matcheur)

        self.polyline = matcheur.polyline


    def reSelect_path(self):
        """ Select on the canvas the path used by the last matching """

        return self.network_layer.select_possible_path()


    def apply_modification( self,type_of_matching : string,
                            matcheur : Matcheur, 
                            speed_column_name : string = None,
                            speed_limit : float = None):
        """ Change the possible path and recalculate the position of the points """

        error = self.network_layer.change_possible_path()

        if error != None:
            return "layer.apply_modification." + error

        try:
            self.path_layer.reset_path()
        except:
            return "layer.apply_modification.path.reset_path.processing"

        try:
            network = self.network_layer.create_vector_from_path()
        except:
            return "layer.apply_modification.network.create_vector_from_path.processing"

        matcheur.set_layers(network, self.path_layer.layer) 

        if type_of_matching == "Matching with Speed" and speed_column_name != None:
            error = self.reduce_path_layer(speed_column_name, speed_limit)
            if error != None:
                return "layer.apply_modification." + error
            
            error = self.path_layer.speed_point_matching(matcheur,speed_column_name,speed_limit)
            if error != None:
                return "layer.apply_modification." + error

        elif type_of_matching == "Matching closest":
            error = self.path_layer.closest_point_matching(matcheur)
            if error != None:
                return "layer.apply_modification." + error

        elif type_of_matching == "Matching by distance":
            error = self.path_layer.distance_point_matching(matcheur)
            if error != None:
                return "layer.apply_modification." + error

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
        if type(mem_layer) == str:
            return "layer.get_polyline." + mem_layer

        return mem_layer