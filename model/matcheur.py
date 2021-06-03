import string

from qgis.core import *
from shapely.geometry import Point

#Import own class
from .import_.leuvenmapmatching.matcher.distance import DistanceMatcher
from .import_.leuvenmapmatching.map.inmem import InMemMap
from .utils.layerTraductor import *
from .utils.geometry import *


class Matcheur:


    def __init__(self, _network_layer : QgsVectorLayer = None, 
                 _path_layer : QgsVectorLayer = None, _OID = "OID"):

        self.network_layer = _network_layer
        self.path_layer = _path_layer

        self.OID = _OID
        self.searching_radius = None
        self.sigma = None

        self.polyline = None


    def set_parameters(self, _searching_radius : float, _sigma : float):
        self.searching_radius = _searching_radius
        self.sigma = _sigma
    

    def set_layers(self,network : QgsVectorLayer,path : QgsVectorLayer):
        self.network_layer = network
        self.path_layer = path


    def verify_input(self):
        """Check for parameters problem."""
 
        if( self.searching_radius is None or
            self.searching_radius < 0 ) :
            return "matcheur.error_searching_radius"

        if (self.sigma is None or 
            self.sigma <=0):
            return "matcheur.error_sigma"

        return True
             

    def find_best_path_in_network(self):
        """ Find the path in the network that 
            has been the most likely taken by the cyclist."""

        #Check parameters validity
        res = self.verify_input()
        if not res:
            return res

        #Convertion to shapely dict
        linelayer = layerTraductor.from_vector_layer_to_list_of_dict(self.network_layer)
        if isinstance(linelayer, str):
            return "matcheur.find_best_path_in_network." + linelayer

        pointlayer = layerTraductor.from_vector_layer_to_list_of_dict(self.path_layer)
        if isinstance(pointlayer,str):
            return "matcheur.find_best_path_in_network." + pointlayer

        pointlayer = layerTraductor.order_list_of_dict(pointlayer,self.OID)
        if isinstance(pointlayer,str):
            return "matcheur.find_best_path_in_network." +pointlayer

        try:
            graph,linedict = build_graph(linelayer)
        except:
            return "matcheur.find_best_path_in_network.geometry.build_graph.error_build_graph"

        #Leveun-mapMatching object
        mymap = InMemMap("mymap", graph=graph, use_latlon=False)
        
        ##Building the path
        pts = []
        for pt in pointlayer:
            pts.append([pt["geometry"].x,pt["geometry"].y])

        dist = self.searching_radius
        sigma = self.sigma

        #Calculate the best path
        try:
            matcher = DistanceMatcher(mymap, max_dist_init=dist, max_dist=dist, obs_noise=sigma, obs_noise_ne=sigma*2,
                                  non_emitting_states=True,only_edges=True)
            states, _ = matcher.match(pts)
        except:
            return "matcheur.find_best_path_in_network.distance_matcher"

        #regrouping every lines
        actualstate = None
        selected_lines = []
        for state in states : 
            if state != actualstate : 
                actualstate = state
                selected_lines.append(linedict[state])
        
        if len(selected_lines) == 0:
            return "matcheur.find_best_path_in_network.empty_best_path"
        #The road tha algorithm think the user took
        self.network_layer = layerTraductor.from_list_of_dict_to_layer(
                selected_lines,
                self.network_layer)

        if isinstance(self.network_layer,str):
            return "matcheur.find_best_path_in_network." + self.network_layer

        #Saving the result
        self.tag_id = [str(feat['joID']) for feat in self.network_layer.getFeatures()]

        #Success
        return None

    
    def snap_points_along_line( self, speedField : string, speedlim : float =1.5 ,
                                minpts : int = 5 , maxpts = float("inf")) : 
        """Snap features along a path using the speed."""


        res = self.verify_input()
        if not res:
            return res , []

        #to dict : No need to check for the outPut result: we controll the input before
        linelayer = layerTraductor.from_vector_layer_to_list_of_dict(self.network_layer)
        pointslayer = layerTraductor.from_vector_layer_to_list_of_dict(self.path_layer)
        pointslayer = layerTraductor.order_list_of_dict(pointslayer,self.OID)

        if len(linelayer) == 0:
            print("Can't match on empty line: don't forget to select the layer")
            return "macheur.snap_points_along_line.empty_layer", []


        polyline = build_polyline(linelayer, pointslayer, 15, 
                                  self.searching_radius, self.sigma)
        if polyline is None:
            return ("matcheur.snap_points_along_line.empty_polyline", [])
        
        self.polyline = polyline

        rev_polyline = reverse_line(polyline)
        length_polyline = polyline.length

        #Identify when the features that are mooving or at a stop
        listpoints = self.move_and_stops(pointslayer, speedField ,
                                         speedlim,lim=speedlim,
                                         minpts = minpts, maxpts=maxpts)
        
        #Iterate on theses list of points and position them according to their state
        accdist = 0
        prevpt = listpoints[0][1][0]
        newpts = []
        newdistances = []
        for case, pointset in listpoints :
            if case == "moving"  :
                temppts = [prevpt]+pointset
                lastpt = pointset[-1]
                #Detect wich length is the most logical
                length1 = polyline.project(lastpt)-accdist
                length2 = length_polyline - rev_polyline.project(lastpt) - accdist
                reallength = shapely.geometry.LineString([(pt.x,pt.y) for pt in temppts]).length
                diff1 = abs(length1-reallength)
                diff2 = abs(length2-reallength)
                #If L1 is the best (normal case)
                if diff1<diff2 or diff1==diff2 or abs(diff1-diff2)<0.1 :
                    projdist = length1
                #if L2 is the best (we start from the end)
                else : 
                    projdist = length_polyline - rev_polyline.project(lastpt) -accdist
                #We calculate the ratio of the projected length
                ratio = projdist / reallength
                #then the new position
                distances = [temppts[i].distance(pointset[i]) for i in range(len(pointset))]
                for d in distances : 
                    accdist+=(d*ratio)
                    newpt = polyline.interpolate(accdist)
                    newpts.append(newpt)
                    newdistances.append(accdist)
                prevpt = pointset[-1]
            #Case where there are stops
            else : 
                center = mean_point(pointset, 2)
                centersnap = polyline.interpolate(polyline.project(center))
                #Check the validity of the snapping
                length1 = polyline.project(centersnap)-accdist
                length2 = length_polyline - rev_polyline.project(centersnap) - accdist
                reallength = prevpt.distance(center)
                diff1 = abs(length1-reallength)
                diff2 = abs(length2-reallength)
                #normal case
                if diff1<diff2 or diff1==diff2 or abs(diff1-diff2)<0.1 : 
                    accdist=polyline.project(centersnap)
                #round trip
                else : 
                    accdist= length_polyline - rev_polyline.project(centersnap)
                #Update important parameters
                prevpt = center
                newpts+=[centersnap for i in range(len(pointset))]
                newdistances+=[accdist for i in range(len(pointset))]

        
        too_far_list = []
        for i in range(len(newpts)):
            if newpts[i].distance(pointslayer[i]["geometry"]) > self.searching_radius:
                too_far_list.append(pointslayer[i][self.OID])

        if len(too_far_list)>0:
            too_far_list.append(len(pointslayer))
        return newpts , too_far_list


    def move_and_stops(self,pointslayer,speedField,
                       speedlim,lim=3,minpts = 5, maxpts = 50) : 
        listed = []
        test = {True:"stopped",False:"moving"}

        #Save states of every features: Mooving or not mooving
        for feat in pointslayer : 
            feat["_situation_"] = test[feat[speedField] < speedlim]

        actualsituation = pointslayer[0]["_situation_"]

        #We create groups of points mooving or at a stop
        actualpts = []
        for feat in  pointslayer:
            ## Normal case
            if feat["_situation_"] == actualsituation  :
                actualpts.append(feat["geometry"])
            ## change situation
            else : 
                listed.append([actualsituation,actualpts])
                actualsituation = feat["_situation_"]
                actualpts = [feat["geometry"]]
        listed.append([actualsituation,actualpts])

        #We delete too short case
        newlisted = []
        actualpts = []
        cnt_moving = 0
        cnt_stopped = 0
        for situation,pts in listed : 
            actualpts+=pts
            if situation == "stopped" : 
                cnt_stopped+=len(pts)
            else : 
                cnt_moving+=len(pts)
            if len(actualpts)>=minpts : 
                if cnt_stopped>cnt_moving : 
                    newlisted.append(["stopped",actualpts])
                else : 
                    newlisted.append(["moving",actualpts])
                actualpts = []
                cnt_moving = 0
                cnt_stopped = 0
        if len(actualpts)>0 : 
            situation,pts = newlisted.pop(-1)
            pts+=actualpts
            newlisted.append([situation,pts])

        return newlisted


    def snap_point_to_closest(self):
        """Snap point to the closest location on the polyline."""
        
        #Conversion to shapely dict
        linelayer = layerTraductor.from_vector_layer_to_list_of_dict(self.network_layer)
        pointslayer = layerTraductor.from_vector_layer_to_list_of_dict(self.path_layer)

        pointslayer = layerTraductor.order_list_of_dict(pointslayer,self.OID)


        if len(linelayer) == 0:
            print("Can't match on empty line: don't forget to select the layer")
            return ("matcheur.snap_point_to_closest.empty_layer",[]) 

        #Construction of the polyline
        polyline = build_polyline(linelayer, pointslayer, 15, 
                                  self.searching_radius, self.sigma)
        if polyline is None:
            print("The polyline obtained is empty, please check your parameters")
            return ("matcheur.snap_point_to_closest.empty_polyline", [])
        self.polyline = polyline

        too_far_list = []
        #Snapping point to closest location on the polyline
        for feat in pointslayer :
            
            projection = polyline.project(Point(feat["geometry"].x,feat["geometry"].y))
            point = polyline.interpolate(projection)

            if feat["geometry"].distance(point) > self.searching_radius:
                too_far_list.append(feat[self.OID])

            feat["geometry"] = point

        if len(too_far_list)>0:
            too_far_list.append(len(pointslayer))
        return layerTraductor.from_list_of_dict_to_layer(pointslayer,self.path_layer,"Point", "matched point to closest"), too_far_list


    def snap_point_by_distance(self):
        """Snap point on the best path 
           taking into account the distance between every points."""

        #Conversion to shapely dict
        linelayer = layerTraductor.from_vector_layer_to_list_of_dict(self.network_layer)
        pointslayer = layerTraductor.from_vector_layer_to_list_of_dict(self.path_layer)
        pointslayer = layerTraductor.order_list_of_dict(pointslayer, self.OID)

        

        if len(linelayer) == 0:
            print("Can't match on empty line: don't forget to select the layer")
            return ("matcheur.snap_point_by_distance.empty_layer",[]) 

        #Building the polyline
        polyline = build_polyline(linelayer, pointslayer, 15, 
                                  self.searching_radius, self.sigma)
        if polyline is None:
            return ("matcheur.snap_point_by_distance.empty_polyline",[])
        self.polyline = polyline

        #Stock the distance between every points
        dist_list = []
        length = 0
        for i in range(len(pointslayer)-1):
            dist = pointslayer[i]["geometry"].distance(pointslayer[i+1]["geometry"])
            length += dist
            dist_list.append(dist)
        
        #Get the ratio between the road and the trace
        ratio = polyline.length / length

        too_far_list = []
        #place first point to closest
        point = polyline.interpolate(polyline.project(Point(pointslayer[0]["geometry"].x,pointslayer[0]["geometry"].y)))

        if point.distance(pointslayer[0]["geometry"])>self.searching_radius:
            too_far_list.append(pointslayer[0][self.OID])
        
        pointslayer[0]["geometry"] = point

        #Snap the points according to their distance to the precedent * ratio
        distance = 0
        for i in range(len(pointslayer)-1):
            distance += dist_list[i] * ratio
            point = polyline.interpolate(distance)
            if point.distance(pointslayer[i+1]["geometry"]) > self.searching_radius :
                too_far_list.append(pointslayer[i+1][self.OID])
            pointslayer[i+1]["geometry"] = point

        
        if len(too_far_list)>0: 
            too_far_list.append(len(pointslayer))
        return layerTraductor.from_list_of_dict_to_layer(pointslayer,self.path_layer,"Point", "matched point by distance"), too_far_list
            


    







