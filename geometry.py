import shapely
from shapely.geometry import Point
from .pyqtree import *
import collections
import numpy as np
from .leuvenmapmatching.map.inmem import InMemMap
from .leuvenmapmatching.matcher.distance import DistanceMatcher

from .dbscan import dbscan2



#############################################################################
## Fonction d'indexation spatiale
#############################################################################


def build_sp_index(geometries) : 
    """ Create a spatial index pyqtree

    Input: 
    geometries:   --A list of shapely geometries

    Output:
    sp_index      -- An object of class pyqtree.Index
    """

    maxX = max([geom.bounds[2] for geom in geometries])
    minX = max([geom.bounds[0] for geom in geometries])
    maxY = max([geom.bounds[3] for geom in geometries])
    minY = max([geom.bounds[1] for geom in geometries])
    

    sp_index = Index((minX,minY,maxX,maxY))
    

    for geom in geometries : 
        sp_index.insert(geom,geom.bounds)
    
    return sp_index


## permet de recuperer dans un index spatial la geometry
## la plus proche d'une autre en entree dans un certain rayon
def NearestGeometry(geom,sp_index,search_dist) : 
    """Return the closest entity in a radius.
    
    Input:
    geom:       -- A shapely geometry
    sp_index    -- An object of class pyqtree.Index
    search_dist -- A double 

    Output:
    The closest entity to geom in search_dist radius
    """

    candidates = sp_index.intersect(geom.buffer(search_dist).bounds)
    distances = [(candidate, candidate.distance(geom)) for candidate in candidates]
    distances.sort(key=lambda x:x[1])
    return distances[0][0]


def mean_point(points, digit) : 
    """Return a point with the average position of every points in points

    Input:
    points:  -- A list of shapely.geometry.point.Point
    digit:   -- A double to controll the truncation

    Output:
    A Point of type : shapely.geometry.point.Point
    
    """
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


def truncate_coords(line,digit) : 
    """Truncates a shapely.geometry.LineString with a precision of digit."""

    coords = list(line.coords)
    newpts = [(truncate(c[0],digit),truncate(c[1],digit)) for c in coords]
    return shapely.geometry.LineString(newpts)


def truncate_coords_pts(point,digit) : 
    """Truncate a shapely.geometry.Point with a precision of digit"""

    return shapely.geometry.Point(truncate(point.x,digit),truncate(point.y,digit))


def reverse_line(line) : 
    """Reverse the order of the vertices in the line"""

    coords = list(line.coords)
    coords.reverse()
    return shapely.geometry.LineString(coords)


def get_extremites(line) : 
    """Return a tuple with the extemities of the line"""
    coords = list(line.coords)
    p1 = shapely.geometry.Point(coords[0])
    p2 = shapely.geometry.Point(coords[-1]) 
    return (p1,p2)


def cut_line(line, points):
    """ Cut a line at given points

    Input:
    line:   -- A shapely.geometry.LineString object
    points  -- A list of shapely.geometry.Point object

    Output:
    lines : -- A list of LineString
    """

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


def cut_line_between(line,p1,p2) : 
    """Cut a line between two points
    
    Input:
    line:   -- A shapely.geometry.LineString object
    p1      -- A shapely.geometry.Point object
    p2      -- A shapely.geometry.Point object
    Output:
    A new shapely.geometry.LineString Object 

    """
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


def to_simple_lines(line) : 
    """Divide a multi LineString into several single LineString
    
    Input:
    line       -- A shapely.geometry.LineString object

    Output:
    new_lines  -- A list of shapely.geometry.LineString object
    """

    new_lines = []
    coords = list(line.coords)
    for i in range(len(coords)-1) : 
        new_lines.append(shapely.geometry.LineString([coords[i], coords[i+1]]))
    return new_lines


def connect_lines(l1,l2) : 
    """Merge two lineString if at least one of their extremities are connected together
    
    Input:
    l1:     -- A shapely.geometry.LineString object
    l2      -- A shapely.geometry.LineString object

    Output:
    A shapely.geometry.LineString object obtained by merging the two lines
    """

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
    """Cut a line every distance cm

    Input:
    line:     -- A shapely.geometry.LineString object
    distance: -- A double

    Output:
    segments  -- A shapely.geometry.LineString object
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

## input : list of shapely.geometry.Points, float, digits
## output : list of shapely.geometry.Points (consolidated)
def consolidate(points,tol=0.3, progression = None) :
    """ Merge every points in a list of points that are close to each other in a radius of 0.3

    Input:
    points:     -- A list of shapely.geometry.Point
    tol:        -- A double representing the radius of research
    digits      -- An int representing the precision of the truncation
    
    Output:
    new_pts:    -- A list of shapely.geometry.Point consolidated
    """

    Xs = np.array([pt.x for pt in points])
    Ys = np.array([pt.y for pt in points])
    XY = np.column_stack([Xs, Ys])
    scanner = dbscan2(XY, tol, 1)
    scanner.fit()
    labels = scanner.df[:,2]
    new_pts = []
    for label in np.unique(labels) : 
        subpts = XY[labels == label]
        new_pts.append(shapely.geometry.Point(np.mean(subpts, axis = 0)))
    return new_pts


        
        
## input : shapely.geometry.LineString,
## output : list of shapely.geometry.LineString
## deux LineString obtenue apres decoupage de l'input en son centre
## NOTE : si utilise avec QGIS, il faudra penser a duppliquer les 
## attributs de la features en cours de modification
## si on decoupe un rond point en deux lignes, chacune de ces lignes
## doit heriter des attributes du round point (table attributaire)
def SplitLoop(line) : 
    """Cut a lin if it's a loop in two
    
    Input:
    line:   -- A shapely.geometry.LineString object

    Output:
    segments:   -- A list of shapely.geometry.LineString 
    """

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
def build_polyline(linelayer, pointlayer, tol, searching_radius, sigma ) : 
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
    
    searching_radius = 45
    
    #calculer le meilleur chemin
    matcher = DistanceMatcher(mymap, max_dist_init=searching_radius, max_dist=searching_radius, obs_noise=sigma, obs_noise_ne=sigma*2,
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

    if(len(selected_lines)) <= 1:
        print("Error not enough selected line")
        return
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