# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 09:21:19 2021

@author: gelbj
"""

import shapely
from shapely.geometry import Point
import itertools
from .utils.geometry import *


#############################################################################
## Corrections des erreurs topologiques
#############################################################################


def simplify_coordinates(linelayer, digits) : 
    """ Simplify all the features coordinates to a digits

    Input: 
    linelayer   -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    digits:     -- An int to specify where to truncate the number
    
    Output:
    linelayer   --The same list of dict with the geometries simplified
    """

    new_geometries = [truncate_coords(feat["geometry"],digits) for feat in linelayer]
    #print(new_geometries)
    i=0
    for feat in linelayer:
        feat["geometry"] = new_geometries[i]
        i+=1
    return(linelayer)



def deal_with_danglenodes(linelayer, tolerance = 0.01) : 
    """ Cut every lines which are touched by the extremity of another line in two
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    tolerance:  -- A double 

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    """
    
    # Step 1 : Extract every extremities of the lines
    pts = [get_extremites(feat["geometry"]) for feat in linelayer]
    pts = list(itertools.chain.from_iterable(pts))
    
    # Step 2 : check for every line the presence of dangle nodes
    # If one is found: cut the line at the intersection
    sp_index = build_sp_index(pts)
    new_features = []
    
    for feat in linelayer : 
        line = feat["geometry"]
        cut_points = []

        buff = line.buffer(tolerance)

        candidates = sp_index.intersect(buff.bounds)

        ok_candidates = [candidate for candidate in candidates if candidate.distance(line)<tolerance]

        start,end = get_extremites(line)
        for candidate in ok_candidates : 
            if candidate.distance(start) > tolerance and candidate.distance(end) > tolerance : 


                for pt in cut_points : 
                    if candidate.distance(pt) > 0 :
                        cut_points.append(candidate)


        if len(cut_points) > 0 : 

            new_lines = cut_line(line,cut_points)
            for new_line in new_lines : 

                dupp = feat.copy()
                dupp["geometry"] = new_line
                new_features.append(dupp)
        else : 

            new_features.append(feat)
    return new_features


def deal_with_intersections(linelayer, tolerance = 0.01, digits = 3) : #meme
    """ Cut every lines which are intersected by another line in two
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    tolerance:  -- A double 
    digits:     -- A double to controll the truncation

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    """
    

    all_geoms = [feat["geometry"] for feat in linelayer]
    sp_index = build_sp_index(all_geoms)
    new_features = []

    for feat in linelayer :
        inter_points = []
        line = feat["geometry"]

        candidates = sp_index.intersect(line.bounds)
        for candidate in candidates : 

            if candidate.equals(line) == False : 

                inter = candidate.intersection(line)
                if inter.geom_type == "Point" : 
                    inter_points.append(inter)
                elif inter.geom_type == "MultiPoint" : 
                    inter_points+=list(inter.geoms)
        

        start,end = get_extremites(line)
        ok_inter = [truncate_coords_pts(pt,digits) for pt in inter_points if 
                    pt.distance(start)>tolerance and pt.distance(end)>tolerance]

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
def deal_with_closecall(linelayer, progression = None, tolerance = 0.3, digits = 3) : #!=
    """ Join every lines that are close to each other
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    tolerance:  -- A double 
    digits:     -- A double to controll the truncation

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    """

    pts = [get_extremites(feat["geometry"]) for feat in linelayer]
    pts = list(itertools.chain.from_iterable(pts))
    
    conso_points = consolidate(pts, tolerance, progression)
    
    sp_index = build_sp_index(conso_points)
    
    newfeatures = []
    for feat in  linelayer: 
        pts = [shapely.geometry.Point(xy) for xy in list(feat["geometry"].coords)]
        start = pts.pop(0)
        end = pts.pop(-1)
       

        newstart = NearestGeometry(start,sp_index,tolerance*15)

        
        newend = NearestGeometry(end,sp_index,tolerance*15)
        
        dupp = feat.copy()
        new_line =  shapely.geometry.LineString([newstart]+pts+[newend])
        dupp["geometry"] = new_line
        
        newfeatures.append(dupp)
    
    return newfeatures


def cut_loops(linelayer) : 
    """ Cut every loops in two
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type shapely.geometry.LineString
    """
    
    new_features = []

    for feat in linelayer : 

        geoms = SplitLoop(feat["geometry"])
            
        for geom in geoms : 

            dupp = feat.copy()
            dupp["geometry"] = geom
            new_features.append(dupp)
            
    return new_features
