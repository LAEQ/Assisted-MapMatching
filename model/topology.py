import itertools

import shapely

# Import Own Class
from .utils.geometry import *

"""This file store every functions that has to do with topological correction."""

def simplify_coordinates(linelayer, digits): 
    """ Simplify all the features coordinates to a digits.

    Input: 
    linelayer   -- A list of dict containing at least a field [geometry] of type 
                   shapely.geometry.LineString
    digits:     -- An int to specify where to truncate the number
    
    Output:
    linelayer   --The same list of dict with the geometries simplified
    """

    new_geometries = [truncate_coords(feat["geometry"], digits) for feat in linelayer]

    i = 0
    for feat in linelayer:
        feat["geometry"] = new_geometries[i]
        i += 1
    return(linelayer)

def deal_with_danglenodes(linelayer, tolerance=0.01) : 
    """ Cut every lines which are touched by the extremity of another line in two.
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type 
                   shapely.geometry.LineString
    tolerance:  -- A double 

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type 
                      shapely.geometry.LineString
    """

    # Step 1 : Extract every extremities of the lines
    pts = [get_extremities(feat["geometry"]) for feat in linelayer]
    pts = list(itertools.chain.from_iterable(pts))
    
    if pts == []:
        return
    # Step 2 : check for every line the presence of dangle nodes
    # If one is found: cut the line at the intersection
    sp_index = build_sp_index(pts)

    new_features = []

    for feat in linelayer : 
        line = feat["geometry"]
        cut_points = []

        buff = line.buffer(tolerance)

        candidates = sp_index.intersect(buff.bounds)

        ok_candidates = [candidate for candidate in candidates if candidate.distance(line) < tolerance]

        start, end = get_extremities(line)
        for candidate in ok_candidates : 
            if (candidate.distance(start) > tolerance and
                    candidate.distance(end) > tolerance): 

                for pt in cut_points:
                    if candidate.distance(pt) > 0:
                        cut_points.append(candidate)

        if len(cut_points) > 0: 

            new_lines = cut_line(line,cut_points)

            for new_line in new_lines: 
                dupp = feat.copy()
                dupp["geometry"] = new_line
                new_features.append(dupp)
        else:

            new_features.append(feat)
    return new_features


def deal_with_intersections(line_layer, tolerance=0.01, digits=3) :
    """ Cut every lines which are intersected by another line in two
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type 
                   shapely.geometry.LineString
    tolerance:  -- A double 
    digits:     -- A double to controll the truncation

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type 
                      shapely.geometry.LineString
    """

    all_geoms = [feat["geometry"] for feat in line_layer]
    sp_index = build_sp_index(all_geoms)
    new_features = []

    for feat in line_layer:
        inter_points = []
        line = feat["geometry"]

        candidates = sp_index.intersect(line.bounds)
        for candidate in candidates: 

            if not candidate.equals(line): 

                inter = candidate.intersection(line)
                if inter.geom_type == "Point": 
                    inter_points.append(inter)
                elif inter.geom_type == "MultiPoint" : 
                    inter_points += list(inter.geoms)
        

        start,end = get_extremities(line)
        ok_inter = [truncate_coords_pts(pt, digits) for pt in inter_points if 
                    pt.distance(start) > tolerance and pt.distance(end) > tolerance]

        if len(ok_inter) == 0: 
            new_features.append(feat)
        else : 
            segments = cut_line(line,ok_inter)
            for segment in segments: 
                dupp = feat.copy()
                dupp["geometry"] = segment
                new_features.append(dupp)
    return new_features

def deal_with_closecall(linelayer, tolerance=0.3, digits=3) :
    """ Join every lines that are close to each other
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type 
                   shapely.geometry.LineString
    tolerance:  -- A double 
    digits:     -- A double to controll the truncation

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type 
                      shapely.geometry.LineString
    """

    pts = [get_extremities(feat["geometry"]) for feat in linelayer]
    pts = list(itertools.chain.from_iterable(pts))

    conso_points = consolidate(pts, tolerance)

    sp_index = build_sp_index(conso_points)

    newfeatures = []
    for feat in linelayer:
        pts = [shapely.geometry.Point(xy) for xy in list(feat["geometry"].coords)]
        start = pts.pop(0)
        end = pts.pop(-1)


        newstart = nearest_geometry(start,sp_index,tolerance * 15)
        if isinstance(newstart, str):
            return "topology.deal_with_closecall." + newstart
        
        newend = nearest_geometry(end,sp_index,tolerance * 15)
        if isinstance(newend, str):
            return "topology.deal_with_closecall." + newend

        dupp = feat.copy()
        new_line = shapely.geometry.LineString([newstart] + pts + [newend])
        dupp["geometry"] = new_line

        newfeatures.append(dupp)

    return newfeatures

def cut_loops(linelayer) : 
    """ Cut every loops in two
    
    Input:      
    linelayer:  -- A list of dict containing at least a field [geometry] of type 
                   shapely.geometry.LineString

    Output:
    new_features:  -- A list of dict containing at least a field [geometry] of type 
                      shapely.geometry.LineString
    """

    new_features = []

    for feat in linelayer : 

        geoms = SplitLoop(feat["geometry"])

        for geom in geoms : 
            dupp = feat.copy()
            dupp["geometry"] = geom
            new_features.append(dupp)

    return new_features
