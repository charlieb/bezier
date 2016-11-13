from math import sqrt, fabs
from shapely.geometry import Point, Polygon, LinearRing, LineString

def tpoint(p1, p2, t):
    (x1,y1) = p1
    (x2,y2) = p2
    return x1+t*(x2-x1),y1+t*(y2-y1)
def beziersplitatt(bezparms,t):
    (bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3) = bezparms
    m1=tpoint((bx0,by0),(bx1,by1),t)
    m2=tpoint((bx1,by1),(bx2,by2),t)
    m3=tpoint((bx2,by2),(bx3,by3),t)
    m4=tpoint(m1,m2,t)
    m5=tpoint(m2,m3,t)
    m=tpoint(m4,m5,t)
    
    return ((bx0,by0),m1,m4,m),(m,m5,m3,(bx3,by3))


X = 0
Y = 1
def dot(p1, p2):
    return p1[X] * p2[X] + p1[Y] + p2[Y]
def mag(v):
    return sqrt(v[X]**2 + v[Y]**2)
def to_v(line):
    return (line[1][X] - line[0][X], 
            line[1][Y] - line[0][Y])

def distanceToPoint(line, p):
    to_p = (line[0],p)
    line_v = to_v(line)
    to_p_v = to_v(to_p)

    c1 = dot(to_p_v, line_v)
    if c1 <= 0:
        return mag(to_p_v)
    c2 = dot(line_v, line_v)
    if c2 <= c1:
        return mag(to_v((p,line[1])))
    return perpDistanceToPoint(line, p)

def perpDistanceToPoint(line, p):
    v = to_v(line)
    vp = to_v((line[0], p))
    line_len = mag(v)
    if line_len == 0: return NaN
    return fabs(v[X] * vp[Y] - vp[X] * v[Y]) / line_len
        
def compute_max_distance(points):
    """
    What's the max distance between the two control points
    and the start and end points. 
    This is a measure of straightness because if the control points
    lie on the line itself then it's perfectly straight
    """
    line = (points[0], points[3])
    ctl1 = points[1]
    ctl2 = points[2]

    return max(distanceToPoint(line, ctl1), distanceToPoint(line, ctl2))

def subdiv(bzs, flat):
    all_flat = False
    while not all_flat:
        next_bzs = []
        all_flat = True
        for bz in bzs:
            #print(bz, compute_max_distance(bz))
            if compute_max_distance(bz) > flat:
                next_bzs.extend(beziersplitatt(bz, 0.5))
                all_flat = False
            else:
                next_bzs.append(bz)
        bzs = next_bzs
    return bzs


if __name__ == '__main__':
    flat = 0.1
    new_bzs = subdiv([((0,0), (0,5), (0,5), (5,5))], flat/4.)
    for bz in new_bzs:
        print('<path d="M', bz[0][X], bz[0][Y],
                'C', bz[1][X], bz[1][Y], 
                     bz[2][X], bz[2][Y],
                     bz[3][X], bz[3][Y],
                '" fill="none" stroke="black" stroke-width="1.0" />'
                )
    print('<svg/>')

    lines = LinearRing([(5,0)] + [bz[3] for bz in subdiv([((5,0), (5,5), (5,5), (0,5))], flat)])
    bzs = LinearRing([new_bzs[0][0]] + [bz[3] for bz in new_bzs])
    print(lines.intersection(bzs))

    from matplotlib import pyplot

    fig = pyplot.figure(1)
    ax = fig.add_subplot(121)
    x,y = lines.xy
    ax.plot(x,y, color='r')

    x,y = bzs.xy
    ax.plot(x,y)

    for ob in lines.intersection(bzs):
        x,y = ob.xy
        ax.plot(x,y, 'o', color='g', zorder=2)
        
    poly = Polygon(bzs)
    new_lines = lines.difference(poly)

    for line in new_lines:
        x,y = line.xy
        ax.plot(x,y, color='y')
    pyplot.show()






