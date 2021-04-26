# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 09:21:19 2021

@author: gelbj
"""

#shapely:
"""
from shapely.geometry import Point

"""
import shapely
from shapely.geometry import Point
import itertools
from .pyqtree import *
import collections
import numpy as np

    
#############################################################################
## Fonction d'indexation spatiale
#############################################################################

# Permet de creer un index spatial pyqtree
# a partir d'une liste de geometrie
# ceci ferait surement l'objet d'une classe particuliere
## NB : la methode bounds de shapely retourne ceci : minx, miny, maxx, maxy
def build_sp_index(geometries) : 
    # obtenir la bbox complete de toutes les geometries

    maxX = max([geom.bounds[2] for geom in geometries])
    minX = max([geom.bounds[0] for geom in geometries])
    maxY = max([geom.bounds[3] for geom in geometries])
    minY = max([geom.bounds[1] for geom in geometries])
    
    # creer l'index (vide au depart)
    sp_index = Index((minX,minY,maxX,maxY))
    
    # inserer chaque geometries
    for geom in geometries : 
        sp_index.insert(geom,geom.bounds)
    
    return sp_index


## permet de recuperer dans un index spatial la geometry
## la plus proche d'une autre en entree dans un certain rayon
def NearestGeometry(geom,sp_index,search_dist) : 
    candidates = sp_index.intersect(geom.buffer(search_dist).bounds)
    distances = [(candidate, candidate.distance(geom)) for candidate in candidates]
    distances.sort(key=lambda x:x[1])
    return distances[0][0]


def mean_point(points, digit) : 
    mx = truncate(sum([pt.x for pt in points]) / len(points),digit)
    my = truncate(sum([pt.y for pt in points]) / len(points),digit)
    return shapely.geometry.Point(mx,my)

#############################################################################
##Fonctions simples de manipulation de geometries
#############################################################################

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))

## input : shapely.geometry.LineString, integer
## output : shapely.geometry.LineString dont les coordonnees ont ete troncaturees
def truncate_coords(line,digit) : 
    coords = list(line.coords)
    newpts = [(truncate(c[0],digit),truncate(c[1],digit)) for c in coords]
    return shapely.geometry.LineString(newpts)

## input : shapely.geometry.Point, integer
## output : shapely.geometry.Point dont les coordonnees ont ete troncaturees
def truncate_coords_pts(point,digit) : 
    return shapely.geometry.Point(truncate(point.x,digit),truncate(point.y,digit))

## input : shapely.geometry.LineString
## output : shapely.geometry.LineString dont l'ordre des vertex a ete inverse
def reverse_line(line) : 
    coords = list(line.coords)
    coords.reverse()
    return shapely.geometry.LineString(coords)

## input : shapely.geometry.LineString
## output : tuple(shapely.geometry.Point,shapely.geometry.Point)
## respectivement le premier et le dernier point d'une LineString
def get_extremites(line) : 
    coords = list(line.coords)
    p1 = shapely.geometry.Point(coords[0])
    p2 = shapely.geometry.Point(coords[-1]) 
    return (p1,p2)

## input : shapely.geometry.LineString, list of shapely.geometry.Point
## output : list of shapely.geometry.LineString
## un ensemble de LineString obtenu apres decoupage de l'input au niveau des points
def cut_line(line, points):

    # First coords of line
    coords = list(line.coords)

    # Keep list coords where to cut (cuts = 1)
    cuts = [0] * len(coords)
    cuts[0] = 1
    cuts[-1] = 1

    # Add the coords from the points
    coords += [list(p.coords)[0] for p in points]    
    cuts += [1] * len(points)        

    # Calculate the distance along the line for each point    
    dists = [line.project(shapely.geometry.Point(p)) for p in coords]
    # sort the coords/cuts based on the distances    
    coords = [p for (d, p) in sorted(zip(dists, coords))]    
    cuts = [p for (d, p) in sorted(zip(dists, cuts))]          

    # generate the Lines    
    lines = []     
    try:
        for i in range(len(coords)-1):    
            if cuts[i] == 1:    
                # find next element in cuts == 1 starting from index i + 1   
                j = cuts.index(1, i + 1)    
                lines.append(shapely.geometry.LineString(coords[i:j+1]))
        #special case for loops
    except:
        print(shapely.wkt.dumps(line))
        for pt in points:
            print(shapely.wkt.dumps(pt))
        
        raise ValueError("error")



    start,end = get_extremites(line)
    if start.distance(end)<0.0001 : 
        seg = lines.pop(-1)
        pts = [shapely.geometry.Point(xy) for xy in list(seg.coords)]
        pts.append(end)
        lines.append(shapely.geometry.LineString(pts))

    return lines


## input : shapely.geometry.LineString, shapely.geometry.Point,shapely.geometry.Point
## output : shapely.geometry.LineString
## une LineString obteneu apres decoupage de l'input entre deux points
def cut_line_between(line,p1,p2) : 
    d1a = line.project(p1)
    d2a = line.project(p2)
    rev_line = reverse_line(line)
    d1b = rev_line.project(p1)
    d2b = line.length - rev_line.project(p2)
    if d1a <= d1b : 
        d1 = d1a
    else : 
        d1 = d1b
        
    if d2a >= d2b : 
        d2 = d2a
    else : 
        d2 = d2b
    start = line.interpolate(d1)
    end = line.interpolate(d2)
    allpts = [shapely.geometry.Point(xy) for xy in line.coords]
    okpts = [pt for pt in allpts if line.project(pt)>d1 and line.project(pt)<d2]
    okpts = [start]+okpts+[end]
    return shapely.geometry.LineString(okpts)


## input : shapely.geometry.LineString,
## output : list of shapely.geometry.LineString
## deux LineString obtenue apres decoupage de l'input en son centre
## NOTE : si utilise avec QGIS, il faudra penser a duppliquer les 
## attributs de la features en cours de modification
## si on decoupe un rond point en deux lignes, chacune de ces lignes
## doit heriter des attributes du round point (table attributaire)
def SplitLoop(line) : 
    start,end = get_extremites(line)
    if start.distance(end)<0.001 : 
        pts = list(line.coords)
        n = round(len(pts)/2)
        pts1 = pts[0:n]
        pts2 = pts[n-1:len(pts)]
        segments =[shapely.geometry.LineString(pts1),shapely.geometry.LineString(pts2)]
    else : 
        segments = [line]
    return segments


## input : shapely.geometry.Points, list of shapely.geometry.Points, integer, float
## output : list of shapely.geometry.Points (consolidated)
## the output is a list of the points arrond the original one
def pontential_neighbours(point,other_points,maxiter,tol) : 
    i=0
    actuals = [point]
    passedpts = []
    sp_index = build_sp_index(other_points)
    while i < maxiter : 
        newactuals = []
        for pt in actuals : 
            if sum([pt.equals(passed) for passed in passedpts])==0 :
                passedpts.append(pt)
                candidates = sp_index.intersect(pt.buffer(tol).bounds)
                for pt2 in candidates : 
                    if sum([pt2.equals(passed) for passed in passedpts]) == 0:
                        newactuals.append(pt2)
        if len(newactuals)==0 : 
            break
        actuals = newactuals
        i+=1
    return passedpts


## input : list of shapely.geometry.Points, float, digits
## output : list of shapely.geometry.Points (consolidated)
def consolidate(points,tol=0.1,digits=3) : 
    indexing = collections.defaultdict(lambda : None)
    newpoints = []
    for i,point in enumerate(points) :
        if indexing[(point.x,point.y)] is None :
            other_points = points.copy()
            other_points.pop(i)
            neighbours = pontential_neighbours(point,other_points,15,tol)
            for n in neighbours : 
                indexing[(n.x,n.y)]=True
            neighbours.append(point)
            newpoints.append(mean_point(neighbours,digits)) #erreur
    return newpoints
        


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
def deal_with_closecall(linelayer, tolerance = 0.01, digits = 3) : 
    
    ## etape 1 : extraire toutes les extremites des lignes
    pts = [get_extremites(feat["geometry"]) for feat in linelayer]
    pts = list(itertools.chain.from_iterable(pts))
    
    ## on va ensuite consolider cet ensemble de points, cad : 
    ## regrouper les points entre lesquels la distance est < tolerance
    conso_points = consolidate(pts, tolerance, digits)
    
    ## on va se creer un index spatial avec ces points consolides
    sp_index = build_sp_index(conso_points)
    
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
    

def SplitLoop(line) : 
    start,end = get_extremites(line)
    if start.distance(end)<0.001 : 
        pts = list(line.coords)
        n = round(len(pts)/2)
        pts1 = pts[0:n]
        pts2 = pts[n-1:len(pts)]
        segments =[shapely.geometry.LineString(pts1),shapely.geometry.LineString(pts2)]
    else : 
        segments = [line]
    return segments


def cut_loops(linelayer) : 
    new_features = []

    for feat in linelayer : 

        geoms = SplitLoop(feat["geometry"])

        for geom in geoms : 

            dupp = feat.copy()
            dupp["geometry"] = geom
            new_features.append(dupp)
            
    return new_features
