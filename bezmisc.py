from math import sqrt, fabs
from functools import reduce
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

def compute_max_distance(points):
    """
    What's the max distance between the two control points
    and the start and end points. 
    This is a measure of straightness because if the control points
    lie on the line itself then it's perfectly straight
    """
    line = LineString([points[0], points[3]])
    ctl1 = Point(points[1])
    ctl2 = Point(points[2])

#    print('max_dist: %s->%s, %s, %s = %s', line, ctl1, ctl2, max(line.distance(ctl1), line.distance(ctl2)))
    return max(line.distance(ctl1), line.distance(ctl2))

def subdiv(bzs, flat):
    all_flat = False
    while not all_flat:
        next_bzs = []
        all_flat = True
        for bz in bzs:
            #print('max_dist: %s > %s'%(compute_max_distance(bz), flat))
            if compute_max_distance(bz) > flat:
                next_bzs.extend(beziersplitatt(bz, 0.5))
                all_flat = False
            else:
                next_bzs.append(bz)

#        for p in [(bz[0], bz[3]) for bz in next_bzs[1:]]:
#            print('s: ' + str(sqrt((p[0][0] - p[1][0])**2 + (p[0][1] - p[1][1])**2)))
#        print('s: ----- :s')

        bzs = next_bzs
    return bzs


if __name__ == '__main__':
    flat = 0.1
#    new_bzs = subdiv([((0,0), (0,5), (0,5), (5,5))], flat/4.)
#    for bz in new_bzs:
#        print('<path d="M', bz[0][X], bz[0][Y],
#                'C', bz[1][X], bz[1][Y], 
#                     bz[2][X], bz[2][Y],
#                     bz[3][X], bz[3][Y],
#                '" fill="none" stroke="black" stroke-width="1.0" />'
#                )
#    print('<svg/>')

    #lines = LinearRing([(5,0)] + [bz[3] for bz in subdiv([((5,0), (5,5), (5,5), (0,5))], flat)])
    bzs = subdiv([((0,0), (0,5), (5,5), (5,0))], flat) 
    lines = LinearRing([(0,0)] + [bz[3] for bz in bzs])
    #bzs = LinearRing([new_bzs[0][0]] + [bz[3] for bz in new_bzs])
#    print(lines.intersection(bzs))

    from matplotlib import pyplot

    fig = pyplot.figure(1)
    ax = fig.add_subplot(121)
    x,y = lines.xy
    ax.plot(x,y, 'o', color='r')

#    x,y = bzs.xy
    x,y = zip(*reduce(lambda x,y: x+y, bzs))
    ax.plot(x,y, 'x')

#    for ob in lines.intersection(bzs):
#        x,y = ob.xy
#        ax.plot(x,y, 'o', color='g', zorder=2)
#        
#    poly = Polygon(bzs)
#    new_lines = lines.difference(poly)
#
#    for line in new_lines:
#        x,y = line.xy
#        ax.plot(x,y, color='y')
    pyplot.show()

