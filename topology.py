# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 09:21:19 2021

@author: gelbj
"""

import shapely
from shapely.geometry import Point
import itertools
from .geometry import *


#############################################################################
## Corrections des erreurs topologiques
#############################################################################

## fonction 0 : simplifier les coordonnees de toutes les lignes
## en appliquant truncate_coords a chaque linestring
def simplify_coordinates(linelayer, digits) : 
    new_geometries = [truncate_coords(feat["geometry"],digits) for feat in linelayer]
    #print(new_geometries)
    i=0
    for feat in linelayer:
        feat["geometry"] = new_geometries[i]
        i+=1
    return(linelayer)


## fonction 1 : gerer les dangle NODES
## le cas ou l'extremite d'une ligne touche une autre ligne
## mais a ce point de contact, la seconde ligne n'est pas 
## decoupe
## NB : on est ici sur du pseudo-code
def deal_with_danglenodes(linelayer, tolerance = 0.01) : 
    
    # etape 1 : extraire toutes les extremites des lignes
    pts = [get_extremites(feat["geometry"]) for feat in linelayer]
    pts = list(itertools.chain.from_iterable(pts))
    
    # etape2 : pour chaque ligne, verifiee si elle est touchee
    # par un de ces points ailleurs que a ces extremites
    # si c'est le cas, il faudra la decouper avec la fonction cut_line
    # a ce ou ces point(s)
    # pour acceler la procedure, on va utiliser un index spatial
    # pour retrouver rapidement les points proches d'une ligne
    sp_index = build_sp_index(pts)
    new_features = []
    
    for feat in linelayer : 
        line = feat["geometry"]
        cut_points = []
        # on applique un petit tampon pour avoir une certaine tolerance
        buff = line.buffer(tolerance)
        # on retrouve les point potentiellement sur la ligne
        candidates = sp_index.intersect(buff.bounds)
        # pour chacun de ces candidats on calcule sa distance avec la ligne
        # et on garde ceux suffisamment proche (dist < tolerance)
        ok_candidates = [candidate for candidate in candidates if candidate.distance(line)<tolerance]
        # on veut maintenant verifier si un candidat se trouve sur la ligne mais pas son extremite
        # si oui, on l'utilisera comme point de decoupe
        start,end = get_extremites(line)
        for candidate in ok_candidates : 
            if candidate.distance(start) > tolerance and candidate.distance(end) > tolerance : 
                # on veut aussi s'assurer que ce candidat n'est pas deja
                # dans notre selection
                for pt in cut_points : 
                    if candidate.distance(pt) > 0 :
                        cut_points.append(candidate)
        # si on a des points de decoupe : 
        if len(cut_points) > 0 : 
            # on decoupe la ligne sur les points d'intersection
            new_lines = cut_line(line,cut_points)
            for new_line in new_lines : 
                # on dupplique la feature originale et on remplace sa geometrie
                dupp = feat.copy()
                dupp["geometry"] = new_line
                new_features.append(dupp)
        else : 
            # si pas besoin de decoupe, on garde seulement la feature originale
            new_features.append(feat)
    return new_features


## fonction 2 : gerer les intersections franches
## le cas ou deux lignes se croisent mais ne se coupent pas
## NB : on est ici sur du pseudo-code
def deal_with_intersections(linelayer, tolerance = 0.01, digits = 3) : 
    
    # commencons par creer un index spatial avec nos lignes
    all_geoms = [feat["geometry"] for feat in linelayer]
    sp_index = build_sp_index(all_geoms)
    new_features = []
    # nous allons iterer sur chacune des lignes de notre layer
    for feat in linelayer :
        inter_points = []
        line = feat["geometry"]
        # trouvons les lignes qui l'intersect potentiellement
        candidates = sp_index.intersect(line.bounds)
        for candidate in candidates : 
            # on evite de garder la meme linestring
            if candidate.equals(line) == False : 
                # on calcule l'intersection et on la conserve
                inter = candidate.intersection(line)
                if inter.geom_type == "Point" : 
                    inter_points.append(inter)
                elif inter.geom_type == "MultiPoint" : 
                    inter_points+=list(inter.geoms)
        # on a maintenant tous les points d'intersection potentiel
        # on va devoir dropper tous les points etant aux extremites de la ligne en question
         # on va aussi troncaturer les coordonnees
        start,end = get_extremites(line)
        ok_inter = [truncate_coords_pts(pt,digits) for pt in inter_points if 
                    pt.distance(start)>tolerance and pt.distance(end)>tolerance]
       # si on a pas d'intersection, on peut simplement garder la feature originale
        if len(ok_inter) == 0 : 
            new_features.append(feat)
        else : 
            segments = cut_line(line,ok_inter)
            for segment in segments : 
                dupp = feat.copy()
                dupp["geometry"] = segment
                new_features.append(dupp)
    return new_features
                
                
## fonction 3 : gerer les close call
## le cas ou les extremites de deux lignes sont tres proches (tolerance)
## mais ne se rejoignent pas...
## NB : on est ici sur du pseudo-code
def deal_with_closecall(linelayer, progression = None, tolerance = 0.01, digits = 3) : 
    
    ## etape 1 : extraire toutes les extremites des lignes
    pts = [get_extremites(feat["geometry"]) for feat in linelayer]
    pts = list(itertools.chain.from_iterable(pts))

    if(progression is not None):
            progression.emit(30)
    
    ## on va ensuite consolider cet ensemble de points, cad : 
    ## regrouper les points entre lesquels la distance est < tolerance
    conso_points = consolidate(pts, tolerance, digits, progression)

    if(progression is not None):
        progression.emit(70)
    
    ## on va se creer un index spatial avec ces points consolides
    sp_index = build_sp_index(conso_points)

    if(progression is not None):
        progression.emit(90)
    
    #step3 iterer sur les lignes et ajuster leurs extremites
    newfeatures = []
    for feat in  linelayer: 
        pts = [shapely.geometry.Point(xy) for xy in list(feat["geometry"].coords)]
        start = pts.pop(0)
        end = pts.pop(-1)
        #trouver le nouveau point de depart

        newstart = NearestGeometry(start,sp_index,tolerance*15)

        #trouver la nouvelle fin
        newend = NearestGeometry(end,sp_index,tolerance*15)
        
        dupp = feat.copy()
        new_line =  shapely.geometry.LineString([newstart]+pts+[newend])
        dupp["geometry"] = new_line
        
        newfeatures.append(dupp)
    
    return newfeatures


def cut_loops(linelayer) : 
    new_features = []

    for feat in linelayer : 

        geoms = SplitLoop(feat["geometry"])
            


        for geom in geoms : 

            dupp = feat.copy()
            dupp["geometry"] = geom
            new_features.append(dupp)
            
    return new_features
