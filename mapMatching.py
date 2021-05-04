from .leuvenmapmatching.matcher.distance import DistanceMatcher
from .leuvenmapmatching.map.inmem import InMemMap
import collections
from shapely import *
from qgis.core import *

from .layerTraductor import *

from .geometry import *

#project et interpolate

class mapMatching:


    def __init__(self, _network_layer, _path_layer, _layer = None ,progression = None):

        self.network_layer = _network_layer
        self.path_layer = _path_layer
        self.new_layer = _layer

        #print(network_layer)
        #print(path_layer)

        #QgsProject.instance().addMapLayer(new_layer)


    def find_best_path_in_network(self):

        linelayer = layerTraductor.from_vector_layer_to_list_of_dict(self.network_layer)
        pointlayer = layerTraductor.from_vector_layer_to_list_of_dict(self.path_layer)
        
        # lecture d'un ensemble de ligne 
        graph,linedict = build_graph(linelayer)

        mymap = InMemMap("mymap", graph=graph, use_latlon=False)
        ##step2 : construire le chemin
        pts = []
        for pt in pointlayer:
            pts.append([pt["geometry"].x,pt["geometry"].y])


        ## parametres generaux
        distInit = 45
        sigma = 5
        print("Line Selecting -------------------------------------------------")
        #calculer le meilleur chemin
        matcher = DistanceMatcher(mymap, max_dist_init=distInit, max_dist=distInit, obs_noise=sigma, obs_noise_ne=sigma*2,
                              non_emitting_states=True,only_edges=True)
        states, _ = matcher.match(pts)
        print("END Selection -------------------------------------------------")

        #recuperer toutes les lignes
        actualstate = None
        selected_lines = []
        for state in states : 
            if state != actualstate : 
                actualstate = state #state["oid"]
                selected_lines.append(linedict[state])
        
        self.new_layer = layerTraductor.from_list_of_dict_to_layer(selected_lines,self.network_layer)

        self.tag_id = [str(feat['joID']) for feat in self.new_layer.getFeatures()]

        #conserver/ selectionner les lignes dans un nouveau vect?


    # polyline is a simple linestring
    def snap_points_along_line(self, speedField, speedlim=1.5 ,minpts = 5 , maxpts = float("inf")) : 

        #to dict
        linelayer = layerTraductor.from_vector_layer_to_list_of_dict(self.new_layer)
        pointslayer = layerTraductor.from_vector_layer_to_list_of_dict(self.path_layer)

        polyline = build_polyline(linelayer, pointslayer, 15)
        print("Finished build polyline")
        rev_polyline = reverse_line(polyline)
        length_polyline = polyline.length
        #---------------------------------------------------------------------------------
        # step 1 : identifier les passages a l'arret VS en mouvement
        #--------------------------------------------------------------------------------- 
        listpoints = self.move_and_stops(pointslayer, speedField ,speedlim,lim=speedlim,minpts = minpts, maxpts=maxpts)
        print("finishe listPoints")
        #---------------------------------------------------------------------------------
        # step 2 : iterer sur les differents ensembles de points en mouvement ou a l'arret
        # et les repositionner en consequence
        #--------------------------------------------------------------------------------- 
        accdist = 0
        prevpt = listpoints[0][1][0]
        newpts = []
        newdistances = []
        for case, pointset in listpoints :
            if case == "moving"  :
                # un peu de magie ici, j'ai la flemme de tout expliquer
                temppts = [prevpt]+pointset
                lastpt = pointset[-1]
                #enjeu 1 : detecter quelle longueur est la plus realiste
                length1 = polyline.project(lastpt)-accdist
                length2 = length_polyline - rev_polyline.project(lastpt) - accdist
                reallength = shapely.geometry.LineString([(pt.x,pt.y) for pt in temppts]).length
                diff1 = abs(length1-reallength)
                diff2 = abs(length2-reallength)
                #si la longueur 1 est la plus realiste (cas normal)
                if diff1<diff2 or diff1==diff2 or abs(diff1-diff2)<0.1 :
                    projdist = length1
                #si la longueur 2 est la plus realiste (on part alors de la fin de la ligne)
                else : 
                    projdist = length_polyline - rev_polyline.project(lastpt) -accdist
                #calcul du ratio de la distance projetee
                ratio = projdist / reallength
                #calcul des nouvelles positions
                distances = [temppts[i].distance(pointset[i]) for i in range(len(pointset))]
                for d in distances : 
                    accdist+=(d*ratio)
                    newpt = polyline.interpolate(accdist)
                    newpts.append(newpt)
                    newdistances.append(accdist)
                prevpt = pointset[-1]
            #cas des points a l'arret
            else : 
                center = mean_point(pointset, 2)
                centersnap = polyline.interpolate(polyline.project(center))
                #verifions si ce snapping est bon ou de la merde
                length1 = polyline.project(centersnap)-accdist
                length2 = length_polyline - rev_polyline.project(centersnap) - accdist
                reallength = prevpt.distance(center)
                diff1 = abs(length1-reallength)
                diff2 = abs(length2-reallength)
                #cas normal
                if diff1<diff2 or diff1==diff2 or abs(diff1-diff2)<0.1 : 
                    accdist=polyline.project(centersnap)
                #cas ou on est sur un aller retour bien merdique
                else : 
                    accdist= length_polyline - rev_polyline.project(centersnap)
                #mettre a jour les parametres necessaires
                prevpt = center
                newpts+=[centersnap for i in range(len(pointset))]
                newdistances+=[accdist for i in range(len(pointset))]

        print("END FONCTION")
        return newpts,newdistances


    #min pts : nombre minimum de points pour former un aggregat
    #maxpts : nombre maximum de point dans un aggregat
    def move_and_stops(self,pointslayer,speedField,speedlim,lim=3,minpts = 5, maxpts = 50) : 
        listed = []
        test = {True:"stopped",False:"moving"}

        #---------------------------------------------------------------------------------
        # step 1 : On veut savoir pour chaque point s'il est arrete ou non
        #---------------------------------------------------------------------------------
        for feat in pointslayer : 
            feat["_situation_"] = test[feat[speedField] < speedlim]

        actualsituation = pointslayer[0]["_situation_"]

        #---------------------------------------------------------------------------------
        # step 2 : On veut creer des suites de points en mouvement et des suites de point arretes
        #---------------------------------------------------------------------------------
        actualpts = []
        for feat in  pointslayer:
            ## cas normal : on est dans la meme situation
            if feat["_situation_"] == actualsituation  :
                actualpts.append(feat["geometry"])
            ## second cas : on est pas dans la meme situation
            else : 
                listed.append([actualsituation,actualpts])
                actualsituation = feat["_situation_"]
                actualpts = [feat["geometry"]]
        listed.append([actualsituation,actualpts])

        #---------------------------------------------------------------------------------
        # step 3 : Un peu de nettoyage, aggregeons les cas trops courts
        #--------------------------------------------------------------------------------- 
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


    







