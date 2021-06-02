import collections
import numpy as np

import shapely
from shapely.geometry import LineString

#Import own class
try:
    from ..import_.pyqtree import *
    from ..import_.leuvenmapmatching.map.inmem import InMemMap
    from ..import_.leuvenmapmatching.matcher.distance import DistanceMatcher
    from ..import_.dbscan import dbscan2
except ImportError:
    print("Couldn't access the import file, check your path")


#############################################################################
## Spatial indexing function
#############################################################################

def build_sp_index(geometries: list) : 
    """ Create a spatial index pyqtree

    Input: 
    geometries:   --A list of shapely geometries

    Output:
    sp_index      -- An object of class pyqtree.Index
    """

    if geometries == []:
        #print("Error empty input value in build_sp_index")
        return

    maxX = max([geom.bounds[2] for geom in geometries])
    minX = min([geom.bounds[0] for geom in geometries])
    maxY = max([geom.bounds[3] for geom in geometries])
    minY = min([geom.bounds[1] for geom in geometries])

    sp_index = Index((minX,minY,maxX,maxY))
    

    for geom in geometries : 
        sp_index.insert(geom,geom.bounds)
    
    return sp_index


def nearest_geometry(geom,sp_index : Index, search_dist : int) : 
    """Return the closest entity in a radius.
    
    Input:
    geom:       -- A shapely geometry
    sp_index    -- An object of class pyqtree.Index
    search_dist -- A double 

    Output:
    The closest entity to geom in search_dist radius
    """
    if geom == None or sp_index == None or search_dist <= 0:
        return "geometry.nearest_geometry.invalid_input"

    candidates = sp_index.intersect(geom.buffer(search_dist).bounds)

    if len(candidates) == 0:
        #print("No candidate found in a distance of " + str(search_dist) + " around " + str(geom))
        return "geometry.nearest_geometry.no_candidate_found"
    
    distances = [(candidate, candidate.distance(geom)) for candidate in candidates]
    distances.sort(key=lambda x:x[1])
    return distances[0][0]


def mean_point(points : list, digit : int) : 
    """Return a point with the average position of every points in the list points.

    Input:
    points:  -- A list of shapely.geometry.point.Point
    digit:   -- A double to controll the truncation

    Output:
    A Point of type : shapely.geometry.point.Point
    
    """

    if points == None or points == []:
        return "geometry.mean_point.empty_list"

    mx = truncate(sum([pt.x for pt in points]) / len(points),digit)
    my = truncate(sum([pt.y for pt in points]) / len(points),digit)
    return shapely.geometry.Point(mx,my)


#############################################################################
##Fonctions simples de manipulation de geometries
#############################################################################

def truncate(f, n):
    """Truncates/pads a float f to n decimal places without rounding."""

    if n <0:
        n = 0

    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))


def truncate_coords(line,digit) : 
    """Truncates a shapely.geometry.LineString with a precision of digit."""

    if not isinstance(line, shapely.geometry.linestring.LineString):
        #print("Can't truncate " + str(type(line)) + " with truncate_coords")
        return line

    if digit <0:
        digit = 0

    coords = list(line.coords)
    newpts = [(truncate(c[0],digit),truncate(c[1],digit)) for c in coords]
    return shapely.geometry.LineString(newpts)


def truncate_coords_pts(point,digit) : 
    """Truncate a shapely.geometry.Point with a precision of digit"""

    if not isinstance(point, shapely.geometry.point.Point ):
        #print("Can't truncate " + str(type(point)) + " with truncate_coords_pts")
        return point

    if digit <0:
        digit = 0

    return shapely.geometry.Point(truncate(point.x,digit),truncate(point.y,digit))


def reverse_line(line) : 
    """Reverse the order of the vertices in the line."""

    if( not isinstance(line, shapely.geometry.linestring.LineString) or
        line == LineString()):
        #print("Can't reverse " + str(type(line)) + " with reverse_line")
        return line


    coords = list(line.coords)
    coords.reverse()
    return shapely.geometry.LineString(coords)


def get_extremites(line) : 
    """Return a tuple with the extemities of the line."""

    if( not isinstance(line, shapely.geometry.linestring.LineString) or
        line == LineString()):
        #print("Can't reverse " + str(type(line)) + " with reverse_line")
        return line,None
    
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

    if( not isinstance(line, shapely.geometry.linestring.LineString) or 
        line == LineString() ):
        #print("Can't reverse " + str(type(line)) + " with reverse_line")
        return None

    if( not isinstance(points, list) or 
        points == [] or
        not isinstance(points[0], shapely.geometry.point.Point) ):

        #print("Problem with the point " + str(points) + " in reverse line")
        return [line]
        

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
        print("Votre ligne fait des allés retours")



    start,end = get_extremites(line)
    if start.distance(end)<0.0001 : 
        seg = lines.pop(-1)
        pts = [shapely.geometry.Point(xy) for xy in list(seg.coords)]
        pts.append(end)
        lines.append(shapely.geometry.LineString(pts))

    return lines


def cut_line_between(line,p1,p2) : 
    """Cut a line between two points.

    Both points are projected on the line.
    
    Input:
    line:   -- A shapely.geometry.LineString object
    p1      -- A shapely.geometry.Point object
    p2      -- A shapely.geometry.Point object
    Output:
    A new shapely.geometry.LineString Object 

    """

    if( not isinstance(line, shapely.geometry.linestring.LineString) or 
        line == LineString() ):
        return None

    if( not isinstance(p1, shapely.geometry.point.Point) or 
        not isinstance(p2, shapely.geometry.point.Point) ):

        #print("Problem with one of the points " + str(p1) + "--" + str(p2) + " in cut line between")
        return [line]

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
    """Divide a polyLineString into several single LineString.
    
    Input:
    line       -- A shapely.geometry.LineString object

    Output:
    new_lines  -- A list of shapely.geometry.LineString object
    """

    if( not isinstance(line, shapely.geometry.linestring.LineString) or 
        line == LineString() ) :
        return [line]

    new_lines = []
    coords = list(line.coords)
    for i in range(len(coords)-1) : 
        new_lines.append(shapely.geometry.LineString([coords[i], coords[i+1]]))
    return new_lines


def connect_lines(l1,l2) : 
    """Merge two lineString if at least one of their extremities 
       are connected together.
    
    Input:
    l1:     -- A shapely.geometry.LineString object
    l2      -- A shapely.geometry.LineString object

    Output:
    A shapely.geometry.LineString object obtained by merging the two lines
    """

    if( not isinstance(l1, shapely.geometry.linestring.LineString) or 
        not isinstance(l2, shapely.geometry.linestring.LineString) or 
        l2 == LineString() or
        l1 == LineString() ) :
        return None

    s1,e1 = get_extremites(l1)
    s2,e2 = get_extremites(l2)

    #Add a little tolerance to avoid truncation issues
    if( s2.distance(e1) != 0 and s2.distance(e1) >= 0.01 and
        e2.distance(e1) != 0 and e2.distance(e1) >= 0.01 ):

        return None

    if s2.distance(e1)<e2.distance(e1) : 
        c1 = list(l1.coords)
        c2 = list(l2.coords)
        return shapely.geometry.LineString(c1+c2[1:len(c2)])
    else : 
        c1 = list(l1.coords)
        c2 = list(l2.coords)
        c2.reverse()
        return shapely.geometry.LineString(c1+c2[1:len(c2)])


def to_lixels(line,distance) : 
    """Cut a line every distance cm.

    Input:
    line:     -- A shapely.geometry.LineString object
    distance: -- A double

    Output:
    segments  -- A list of shapely.geometry.LineString object
    """

    if( not isinstance(line, shapely.geometry.linestring.LineString) or 
        line == LineString() ) :
        return None

    if distance <=0:
        return [line]

    #Creation of every points on the line
    totdist=0
    length = line.length
    pts = []
    while totdist+distance < length : 
        totdist+=distance
        pts.append(line.interpolate(totdist))
    segments = cut_line(line,pts)
    return segments


def consolidate(points,tol=0.31) :
    """ Merge every points in a list of points that are close to each other 
        in a radius of 0.3.

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


        
        

def SplitLoop(line) : 
    """Cut line in two if it's a loop 
    
    Input:
    line:   -- A shapely.geometry.LineString object

    Output:
    segments:   -- A list of shapely.geometry.LineString 
    """

    if( not isinstance(line, shapely.geometry.linestring.LineString) or 
        line == LineString() ) :
        return None

    start,end = get_extremites(line)
    if start.distance(end)<0.001 : 
        pts = list(line.coords)

        n = round(len(pts)/2)
        if n == 1:
            return [line]
        pts1 = pts[0:n]
        pts2 = pts[n:len(pts)]

        segments =[shapely.geometry.LineString(pts1),shapely.geometry.LineString(pts2)]
    else : 
        segments = [line]


    return segments



####################################################################################
# Polyline generation function
####################################################################################


def build_polyline( linelayer: list, pointlayer: list, tol : float, 
                    searching_radius : float, sigma : float ) : 
    """Create a long linestring from a linelayer, points and a tolerance
       
       The tolerance is important to identify possible round-trip. 
       15 is the recommended value
       
       Input:
       linelayer:           -- A list of dict representing the network 
       pointlayer:          -- A list of dict representing the trace
       tol:                 -- A float
       searching_radius:    -- A float representing the searching range 
                               of the algorithm for every points
        sigma:              -- A float. The bigger he is, the more weight 
                               we give to distant roads
        
        Output:
        cutted_polyline:    -- A list of dict representing the polyline
       """

    # step 1 : Create a set of simple lines cutted every tol cm

    base_lines = []
    cnt = 0
    for feat in linelayer : 
        for sline in to_simple_lines(feat["geometry"]) : 
            lixels = to_lixels(sline, tol)
            if lixels != None:
                for lixel in lixels : 
                    base_lines.append({"OID" : cnt, "geometry" : lixel})
                    cnt+=1
    
    
    # step 2 : Calculate the best path and remove useless elements
    graph,linedict = build_graph(base_lines)
    mymap = InMemMap("mymap", graph=graph, use_latlon=False)
    pts = [(pt["geometry"].x,pt["geometry"].y) for pt in pointlayer]
    

    matcher = DistanceMatcher(mymap, max_dist_init=searching_radius, 
                              max_dist=searching_radius, obs_noise=sigma, 
                              obs_noise_ne=sigma*2,
                              non_emitting_states=True,only_edges=True)
    states, _ = matcher.match(pts)
    actualstate = None
    selected_lines = []
    for state in states : 
        if state != actualstate : 
            actualstate = state
            selected_lines.append(linedict[state]["geometry"])


    # step 3 : Generate a long polyline from the values conserved
    
    if(len(selected_lines)) <= 1:
        print("Error not enough selected line")
        return
    lines = selected_lines
    l2 = lines.pop(0)

    s1,e1 = get_extremites(l2)
    if s1.distance(lines[0])<e1.distance(lines[0]) : 
        c2 = list(l2.coords)
        c2.reverse()
        l2 = shapely.geometry.LineString(c2)
    for l1 in lines : 
        test = connect_lines(l2,l1)
        if test != None:
            l2 = test
        else: 
            """Debugging tool
            d1, f1 = get_extremites(l1) 
            d2, f2 = get_extremites(l2)
            print("-------Error: 2 lines are not connected to each other----------")
            print(d2)
            print(f2)
            print(d1)
            print(f1)
            print("-----------------")
            """
            pass
        
    start = l2.interpolate(l2.project(pointlayer[0]["geometry"]))
    end = l2.interpolate(l2.project(pointlayer[-1]["geometry"]))
    cutted_polyline = cut_line_between(l2,start,end)
        
    return cutted_polyline


def build_graph(linelayer) : 
    """Construct two dictionnary needed to create a graph"""

    allnodes = collections.defaultdict(lambda : None)
    linedict = {}
    #Step one: Get every nodes
    linelayer2 = []

    for feat in linelayer:
        lines = to_simple_lines(feat["geometry"])
        for line in lines:
            dupp = feat.copy()
            dupp["geometry"] = line
            linelayer2.append(dupp)
        


    for feat in  linelayer2: 
        line = feat["geometry"]
        start,end = get_extremites(line)
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