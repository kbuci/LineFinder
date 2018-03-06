from math import atan2
from math import pi
import math 
DELTA = 100000

class Point:
    def __init__(self, frac_x: float, frac_y: float):
        
        self._frac_x = frac_x
        self._frac_y = frac_y
        self._edges = []


    def frac(self) -> (float, float):
      
        return (self._frac_x, self._frac_y)

    def x_coord(self) -> float:
        return self._frac_x

    def y_coord(self) -> float:
        return self._frac_y

    def connect(self, p):
        self._edges.append(p)

    def __eq__(self, other):
        return self._frac_x == other.x_coord() and self._frac_y == other.y_coord()

    def __ne__(self, other):
        return not self.__eq__(other)    

    def equals(self, p):
        return self._frac_x == p.x_coord() and self._frac_y == p.y_coord()
    def edges(self):
        return self._edges
    
    def pixel(self, width: float, height: float) -> (float, float):
     
        return (int(self._frac_x * width), int(self._frac_y * height))

    
    def frac_distance_from(self, p: 'Point') -> float:
        return math.sqrt(
            (self._frac_x - p._frac_x) * (self._frac_x - p._frac_x)
            + (self._frac_y - p._frac_y) * (self._frac_y - p._frac_y))



def from_frac(frac_x: float, frac_y: float) -> Point:
   
    return Point(frac_x, frac_y)



def from_pixel(pixel_x: float, pixel_y: float, width: float, height: float) -> Point:

    return Point(pixel_x / width, pixel_y / height)

class point_line:
    def __init__(self, pointPair: (Point)):
       
        if pointPair[0].x_coord() < pointPair[1].x_coord():
            self._p1 , self._p2 = pointPair
        elif pointPair[1].x_coord() < pointPair[0].x_coord():
            self._p2, self._p1 = pointPair
        else:
            if pointPair[0].y_coord() < pointPair[1].y_coord():
                self._p1, self._p2 = pointPair
            else:
                self._p2, self._p1 = pointPair
                
        self._calcSlope()

    def _calcSlope(self):
        x1, y1 = self._p1.frac()
        x2, y2 = self._p2.frac()
        try:
            self._slope = (y1 - y2)/(x1 - x2)
        except:
            self._slope = DELTA

    def slope(self) ->float or None:
        return self._slope

    def angle(self, pivot) -> float:
        y_diff, x_diff = self._p2.y_coord() - self._p1.y_coord(), self._p2.x_coord() - self._p1.x_coord()
        if pivot == self._p1:
            ang =  atan2(y_diff, x_diff)
        elif pivot == self._p2:
            ang = atan2(-y_diff, -x_diff)
        return ang if ang > 0 else ang + 2 * pi
      
        
        
    

    def start(self) -> float:
        return self._p2

    def end(self) -> float:
        return self._p1

    def f_x(self, x: float) -> float:
        m =  self._slope * (x - self._p1.x_coord()) + self._p1.y_coord()
       
        return m
        
        
    def _in_bounds(self, line, exclude_endpoints=False):
        x, y = self.intersection_point(line)
        '''
        x_diff = (DELTA if exclude_endpoints else 0)
        y_diff = (self.f_x(self._p1.x_coord() + DELTA) - self._p1.y_coord() if exclude_endpoints else 0)
        '''
        domain_a = (self._p1.x_coord() , self._p2.x_coord() )
        domain_b = (line.end().x_coord(), line.start().x_coord())
        range_a = (min(self._p1.y_coord(), self._p2.y_coord()), max(self._p1.y_coord(), self._p2.y_coord()))
        range_b = (min(line.start().y_coord(), line.end().y_coord()), max(line.start().y_coord(), line.end().y_coord()))
        return (domain_a[0] <= x) and (domain_a[1] >= x) and (domain_b[0] <= x ) and (domain_b[1] >= x) and (range_a[0] <= y) and (range_a[1] >= y) and (range_b[0] <= y) and (range_b[1] >= y)
        #return ((domain_a[0] <= domain_b[0] and domain_a[1] >= domain_b[0]) or (domain_a[0] <= domain_b[1] and domain_a[1] >= domain_b[1]))
      #and ((range_a[0] <= range_b[0] and range_a[1] >= range_b[0]) or (range_a[0] <= range_b[1] and range_a[1] >= range_b[1]))
        
    def intersection_point(self, line):
        x = (self.slope() * self.end().x_coord() - self.end().y_coord() - line.slope() * line.end().x_coord() + line.end().y_coord())
        x /= self.slope() - line.slope()

        return (x, self.f_x(x))
       
    def limit(self, point):
        if point == self._p1:
            x_coordinate = self._p1.x_coord() + 10**-4
        elif point == self._p2:
            x_coordinate = self._p2.x_coord() - 10**-4
        return Point(x_coordinate, self.f_x(x_coordinate))

        
        
    def intersects(self, line):
       
            
        if self.slope() == line.slope():
            return False
       
        if self._in_bounds(line):
            #print(self.intersection_point(line))
            #print(line.end().y_coord())
           
            #print(line.start().y_coord())
            #if ((self.f_x(line.end().x_coord()) >= line.end().y_coord()) and (self.f_x(line.start().x_coord()) <= line.start().y_coord())) or ((self.f_x(line.end().x_coord()) <= line.end().y_coord()) and (self.f_x(line.start().x_coord()) >= line.start().y_coord())):
                return True

        return False

    def contains_point(self, point):
        if self.f_x(point.x_coord()) == point.y_coord() and point.x_coord() >=  self._p1.x_coord() and point.x_coord() <= self._p2.x_coord():
            return True
        return False

    def __eq__(self, other):
        return self.start() == other.start() and self.end() == other.end()

    def __ne__(self, other):
        return not(self.__eq__(other))

    def mag(self):
        return math.sqrt((self._p1.x_coord() - self._p2.x_coord())**2 + (self._p1.y_coord() - self._p2.y_coord())**2)
    

        

class line_system:
    def __init__(self, startPos, boundaries):
        self._nodes = dict()
        self._lines = boundaries
        #self._destination = endPos
        self._points = [startPos]

    def add_point_line(self, line):
        includeStart = True
        includeEnd = True
        for segment in self._lines:
            hasStart = not segment.contains_point(line.start())
            hasEnd = not segment.contains_point(line.end())
            if not (hasStart or hasEnd):
                return
            includeStart = includeStart and hasStart
            includeEnd = includeEnd and hasEnd
        self._lines.append(line)
        self._points += [line.start()] if includeStart else []
        self._points += [line.end()] if includeEnd else []
            
        '''
        adjacent_lines = []
        for segment in self._lines:
            adjacent_lines += ([segment] if line.intersects(segment) else []) 
        if not any(l.contains_point(line.end()) and l.contains_point(line.start()) for l in adjacent_lines):
            self._lines.append(line)
            self._points += [line.start()] if line.start() not in self._points else []
            self._points += [line.end()] if line.end() not in self._points else []
            '''
        
    def connect(self, initPair, finalPoint):
        initPoint, ang_range = initPair
        edge = point_line((initPoint, finalPoint))
        #ang = edge.angle(initPoint)
        
        severed_edge = point_line((edge.limit(initPoint), edge.limit(finalPoint)))
        
        '''inverse = False
        if ang_range[0] > ang_range[1]:
            inverse = True
            ang_range = (ang_range[1], ang_range[0])
            ang += 3.14
            ang -= 2* 3.14 if ang > 2 * 3.14 else 0   
        if ang < ang_range[0] or ang > ang_range[1]:
            if not inverse: 
                return []
        else:
            if inverse:
                return []'''
        for line in self._lines:
            if severed_edge.intersects(line): #'''and not (line.contains_point(finalPoint) or line.contains_point(initPoint))'''
                return None
        return ( edge, finalPoint)  

#     def build_nodes(self, startPos, start_range):
#         #interest_points = []
#         exploring = [(startPos, start_range )]
#         points = self._points
#         connection_points = set()
#         for pt, range in exploring:
#             pair = (pt.x_coord(), pt.y_coord())#o(n)
#             print(pair)
#             if (pair, range) not in connection_points:
#                 connection_points.add((pair, range))
#                 
#                 if not((pair, range) in self._nodes):
#                     self._nodes[(pair, range)] = []
#                     for pt2 in points:#o(n)
#                         if not any(pt2 == p[0] for p in exploring):
#                         
# #                         if 
# #                         comprimised_edges = [line for line in self._nodes[(pair, range)] if line.contains_point(pt2)]
# #                         if comprimised_edges:
# #                             for line in comprimised_edges:
# #                                 self._nodes[(pair, range)].remove(line)
# #                                 edge = []
# #                         else
#                             edge = self.connect((pt, range), pt2)#o(n)
#                     
#                             if edge != []:
#                     #interest_points += [pt2] if pt2 not in interest_points else []
#                                 self._nodes[(pair, range)] += edge
#                                 exploring += [(pt2, self.angle_range(edge[0], pt2))] 


                      
        
        #remaining_points = [Point(*pair[0]) for pair in self._nodes]
        #self._points = remaining_points
                #note to self pop() faster than pop(n)
        #self._points = interest_points
    
    def build_nodes(self, start_range):
        #interest_points = []
        exploring = [self._points[0]]
        explored = set()
        points = self._points.copy()
        #connection_points = set()
        print(exploring[0] in points)
        print(points)
        for pt in exploring:
            print(pt in points)
            pair = (pt.x_coord(), pt.y_coord())#o(n)
            print(pair)
            #points.remove(pt)
            if not(pair in explored):
                explored.add(pair)
                #if not(pair in self._nodes):
                self._nodes[pair] = []
                points.remove(pt)
                for pt2 in points:#o    (n)
                            
    #                         if 
    #                         comprimised_edges = [line for line in self._nodes[(pair, range)] if line.contains_point(pt2)]
    #                         if comprimised_edges:
    #                             for line in comprimised_edges:
    #                                 self._nodes[(pair, range)].remove(line)
    #                                 edge = []
    #                         else
                    edge = self.connect((pt, (-2, 20)), pt2)#o(n)
                    
                    if edge:
                    #interest_points += [pt2] if pt2 not in interest_points else []
                        
                        self._nodes[pair].append(edge)
                        exploring.append(pt2)
            
        
        for pt in self._points:
            pair = (pt.x_coord(), pt.y_coord())
            if pair not in self._nodes:
                self._points.remove(pt)
             
    def refresh(self ):
       
        lastLine = self._lines[-1]
        newNodes = { lastLine.start().frac() : [], lastLine.end().frac() : []}
        for node in self._nodes:
            nodePoint = Point(*node)
            
            newNodes[node] = []
            for edge, pt in self._nodes[node]:
                if not edge.intersects(lastLine):
                    newNodes[node].append((edge, pt))
                
            
            line1 = self.connect((nodePoint, (-2, 20)), lastLine.start())
            line2 = self.connect((nodePoint, (-2, 20)), lastLine.end())
            
            if line1:
                line1 = line1[0]
                newNodes[node].append((line1, lastLine.start()))
                newNodes[lastLine.start().frac()].append((line1, nodePoint))
            if line2:
                line2 = line2[0]
                newNodes[node].append((line2, lastLine.end()))
                newNodes[lastLine.end().frac()].append((line2, nodePoint))

            if newNodes[node] == []:
                del newNodes[node]
            
        self._nodes = newNodes
        
        
    def node_reset(self):
        self._nodes = {} 
    def angle_range(self, line, pt)->(float, float):
        adj = []
        for segment in self._lines:
            if segment.contains_point(pt) and segment != line:
                if pt == segment.end() or pt == segment.start():
                    adj.append(segment)
                else:
                    #divides line about Point pt
                    adj += [point_line((segment.end(), pt)), point_line((segment.start(), pt))]
        if len(adj) == 0:
            return (-1, 9)
        
        print(adj)   
        #return (min(adj, key=lambda x: x.angle(pt) - line.angle(pt)).angle(pt), min(adj, key=lambda x: line.angle(pt) - x.angle(pt)).angle(pt))
        returned =  (min(adj, key=lambda ang: self._rotate_range(ang.angle(pt), line.angle(pt))), max(adj, key=lambda ang: self._rotate_range(ang.angle(pt), line.angle(pt))))
        return(returned[0].angle(pt), returned[1].angle(pt))
    def _rotate_range(self, a, b):
        diff = b + 3.14 * 2 - a
        return diff if diff < 2 * 3.14 else diff - 3.14 * 2   
            
        
        
        

    
             
    
    
            
if __name__ == '__main__':
    line1 = point_line((Point(0, 0), Point(-5, 0)))
    
    print(line1.angle(Point(0,0)))
    l = line_system(Point(0,0), [])
    #l.add_point_line(line1)
    l.add_point_line(point_line((Point(-2,-2), Point(2, 2))))
    l.add_point_line(point_line((Point(0,0), Point(-2, 2))))
    print(l.angle_range(line1, Point(0,0)))
    print(line1.intersects(l._lines[0]))
    
