import shapely
from shapely.geometry import Point
from .pyqtree import *
import collections
import numpy as np
from .leuvenmapmatching.map.inmem import InMemMap
from .leuvenmapmatching.matcher.distance import DistanceMatcher



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

# input : une shapely LineString
# output : une liste de shapely LineString
# decoupe la linestring originale a chacun de ses noeuds
def to_simple_lines(line) : 
    new_lines = []
    coords = list(line.coords)
    for i in range(len(coords)-1) : 
        new_lines.append(shapely.geometry.LineString([coords[i], coords[i+1]]))
    return new_lines


# input : deux shapely linestring dont au moins une extremite se touche
# output une linestring etant la concatenation des deux
def connect_lines(l1,l2) : 
    s1,e1 = get_extremites(l1)
    s2,e2 = get_extremites(l2)
    if s2.distance(e1)<e2.distance(e1) : 
        c1 = list(l1.coords)
        c2 = list(l2.coords)
        return shapely.geometry.LineString(c1+c2)
    else : 
        c1 = list(l1.coords)
        c2 = list(l2.coords)
        c2.reverse()
        return shapely.geometry.LineString(c1+c2)


# input : une shapely LineString et une distance de decoupage
# output : une liste de shapely LineString
# decoupe la linestring originale selon une distance definie
def to_lixels(line,distance) : 
    """
    Fonction permettant de lixeliser un geodataframe de lignes
    """
    #creation de tous les points sur la ligne
    totdist=0
    length = line.length
    pts = []
    while totdist+distance < length : 
        totdist+=distance
        pts.append(line.interpolate(totdist))
    segments = cut_line(line,pts)
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
def consolidate(points,tol=0.1,digits=3, progression = None) :
    """
    input: 
    liste de points: avec des points proches de distance < tol entre eux
    chaque points: - de tol de lui : utiliser bounding box
    map : points visité


    output: liste de points [shapelypts,...]

    """
    indexing = collections.defaultdict(lambda : None)
    newpoints = []

    #points_list = points.copy()

    print("Start")

    for i in range(len(points)):
        if((indexing[(points[i].x,points[i].y)] is not None)):
            #print(str(i) + ": ALREADY USED BEFORE")
            continue
        
        ma_list = []

        ma_list = consolidate_worker(points,tol,indexing,ma_list,i)
                
        for point in ma_list:
            indexing[(point.x,point.y)] = True

        if len(ma_list) > 1:
            newpoints.append(mean_point(ma_list,digits))
        else:
            newpoints.append(points[i])

    print("END")

    return newpoints

def consolidate_worker(points,tol,indexing,ma_list,position):
    point = points[position]

    return_list = ma_list
    return_list.append(point)

    #del points[position]

    for i in range(len(points)):
        if((indexing[(points[i].x,points[i].y)] is not None) or (points[i] in return_list) or (points[i].distance(point) > tol)):
            #print(str(i) + ": ALREADY USED BEFORE")
            continue

        return_list = consolidate_worker(points,tol,indexing,return_list,i)
        

    return return_list
                
        
        
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
        if n == 1:
            return [line]
        pts1 = pts[0:n]
        pts2 = pts[n-1:len(pts)]

        segments =[shapely.geometry.LineString(pts1),shapely.geometry.LineString(pts2)]
    else : 
        segments = [line]


    return segments


####################################################################################
####################################################################################
# FONCTION DE GENERATION D'UNE POLYLIGNE
####################################################################################
####################################################################################

# a partir d'un ensemble de ligne, de point et d'une tolerance
# generer une seule longue linestring qui pourra etre utilisee
# pour ajuster les points dessus. Tolerance est important pour 
# le cas des aller-retour sur une meme ligne, plus la tolerance
# est petite, plus on pourra identifier clairement le point de retoure
# NB : possibilite de bcp optimiser en decoupant uniquement les lignes
# sur lesquelles ce serait necessaire : les lignes pour lesquels
# le debut ne coincide pas avec la prochaine.
# valeur recommandee pour tol actuellement : 15
def build_polyline(linelayer, pointlayer, tol) : 
    #---------------------------------------------------------------------------------
    # step 1 : creer un ensemble de lignes simples et decoupee selon une distance = tol
    #---------------------------------------------------------------------------------
    base_lines = []
    cnt = 0
    for feat in linelayer : 
        for sline in to_simple_lines(feat["geometry"]) : 
            for lixel in to_lixels(sline, tol) : 
                base_lines.append({"OID" : cnt, "geometry" : lixel})
                cnt+=1
    
    #---------------------------------------------------------------------------------
    # step 2 : a partir de cet ensemble de segments simples, recalculer le chemin le plus
    # probable. L'idee etant de se debarasser ainsi de tous les elements superflus
    #---------------------------------------------------------------------------------
    graph,linedict = build_graph(base_lines)
    mymap = InMemMap("mymap", graph=graph, use_latlon=False)
    ##step2 : construire le chemin
    pts = [(pt["geometry"].x,pt["geometry"].y) for pt in pointlayer]
    
    distInit = 45
    sigma = 5
    
    #calculer le meilleur chemin
    matcher = DistanceMatcher(mymap, max_dist_init=distInit, max_dist=distInit, obs_noise=sigma, obs_noise_ne=sigma*2,
                          non_emitting_states=True,only_edges=True)
    states, _ = matcher.match(pts)
    actualstate = None
    selected_lines = []
    for state in states : 
        if state != actualstate : 
            actualstate = state
            selected_lines.append(linedict[state]["geometry"])


    #---------------------------------------------------------------------------------
    # step 3 : Generer une longue polyligne a partir de tous les segments retenus
    #---------------------------------------------------------------------------------
    lines = selected_lines
    l2 = lines.pop(0)

    s1,e1 = get_extremites(l2) #€rror
    if s1.distance(lines[0])<e1.distance(lines[0]) : 
        c2 = list(l2.coords)
        c2.reverse()
        l2 = shapely.geometry.LineString(c2)
    for l1 in lines : 
        l2 = connect_lines(l2,l1)
        
    start = l2.interpolate(l2.project(pointlayer[0]["geometry"]))
    end = l2.interpolate(l2.project(pointlayer[-1]["geometry"]))
    cutted_polyline = cut_line_between(l2,start,end)
        
    return cutted_polyline


    # fonction permetttant de creer les deux dictionnaires necessaires a la creation d'un graph
def build_graph(linelayer) : 
    allnodes = collections.defaultdict(lambda : None)
    linedict = {}
    #Etape 1 : recuperer tous les noeuds
    for feat in  linelayer: 
        line = feat["geometry"]
        start,end = get_extremites(line)
        #les extremites de la lignes sont des points
        #on definit leur nom par la concatenation des leur coordonnes geographique
        p1 = str(truncate(start.x,2))+"_"+str(truncate(start.y,2))
        p2 = str(truncate(end.x,2))+"_"+str(truncate(end.y,2))
        linedict[(p1,p2)]=feat
        linedict[(p2,p1)]=feat
        if allnodes[p1] is None : 
            allnodes[p1] = ((truncate(start.x,2),truncate(start.y,2)),[])
        if allnodes[p2] is None : 
            allnodes[p2] = ((truncate(end.x,2),truncate(end.y,2)),[])
        if p1 not in allnodes[p2][1] : 
            allnodes[p2][1].append(p1)
        if p2 not in allnodes[p1][1] : 
            allnodes[p1][1].append(p2)

    return (allnodes,linedict)