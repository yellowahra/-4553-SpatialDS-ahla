"""
@author - AHLA CHO
@date -  10/05/2015
@description - THREE POLYGONES AND THREE POINTS ARE MOVING
            AND IF POINTS ARE IN THE POLYGONES, THEY ARE CHANGED COLOR
            AND IF POLYGONES ARE COLLISION, THEY ARE CHANGE THE DIRECTION
"""
"""Point and Rectangle classes.
This code is in the public domain.
Point  -- point with (x,y) coordinates
Rect  -- two points, forming a rectangle
"""
import pantograph
import math
import sys


class Point:

    """A point identified by (x,y) coordinates.
    supports: +, -, *, /, str, repr
    length  -- calculate length of vector to point from origin
    distance_to  -- calculate distance between two points
    as_tuple  -- construct tuple (x,y)
    clone  -- construct a duplicate
    integerize  -- convert x & y to integers
    floatize  -- convert x & y to floats
    move_to  -- reset x & y
    slide  -- move (in place) +dx, +dy, as spec'd by point
    slide_xy  -- move (in place) +dx, +dy
    rotate  -- rotate around the origin
    rotate_about  -- rotate around another point
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        set.direction="S"

    def __add__(self, p):
        """Point(x1+x2, y1+y2)"""
        return Point(self.x+p.x, self.y+p.y)

    def __sub__(self, p):
        """Point(x1-x2, y1-y2)"""
        return Point(self.x-p.x, self.y-p.y)

    def __mul__( self, scalar ):
        """Point(x1*x2, y1*y2)"""
        return Point(self.x*scalar, self.y*scalar)

    def __div__(self, scalar):
        """Point(x1/x2, y1/y2)"""
        return Point(self.x/scalar, self.y/scalar)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()

    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)

    def clone(self):
        """Return a full copy of this point."""
        return Point(self.x, self.y)

    def integerize(self):
        """Convert co-ordinate values to integers."""
        self.x = int(self.x)
        self.y = int(self.y)

    def floatize(self):
        """Convert co-ordinate values to floats."""
        self.x = float(self.x)
        self.y = float(self.y)

    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y

    def slide(self, p):
        '''Move to new (x+dx,y+dy).
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + p.x
        self.y = self.y + p.y

    def slide_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy).
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + dx
        self.y = self.y + dy

    def rotate(self, rad):
        """Rotate counter-clockwise by rad radians.
        Positive y goes *up,* as in traditional mathematics.
        Interestingly, you can use this in y-down computer graphics, if
        you just remember that it turns clockwise, rather than
        counter-clockwise.
        The new position is returned as a new Point.
        """
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
        return Point(x,y)

    def rotate_about(self, p, theta):
        """Rotate counter-clockwise around a point, by theta degrees.
        Positive y goes *up,* as in traditional mathematics.
        The new position is returned as a new Point.
        """
        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
        result.slide(p.x, p.y)
        return result

    def set_direction(self,direction):
        assert direction in ['N','NE','E','SE','S','SW','W','NW']

        self.direction = direction
    def get_direction(self):
        return self.direction

    def update_position(self, window):
        if self.x <= 0:
            if self.direction == "W":
                self.direction = "E"
            if self.direction == "NW":
                self.direction="NE"
            if self.direction =="SW":
                self.direction ="SE"
        if self.y<=0:
            if self.direction =="N":
                self.direction="S"
            if self.direction =="NE":
                self.direction="SE"
            if self.direction =="NW":
                self.direction="SW"
        if self.x>=window.width:
            if self.direction=="E":
                self.direction="W"
            if self.direction=="SE":
                self.direction="SW"
            if self.direction=="NE":
                self.direction="NW"
        if self.y>=window.height:
            if self.direction=="S": #N S
                self.direction="N"
            if self.direction=="SE":
                self.direction="NE"
        if self.direction == "N":
            self.y -= 1
        if self.direction == "NE":
            self.y -= 1
            self.x += 1
        if self.direction == "E":
            self.x += 1
        if self.direction == "SE":
            self.x += 1
            self.y += 1
        if self.direction == "S":
            self.y += 1
        if self.direction == "SW":
            self.x -= 1
            self.y += 1
        if self.direction == "W":
            self.x -= 1
        if self.direction == "NW":
            self.y -= 1
            self.x -= 1



class Rect:

    """A rectangle identified by two points.
    The rectangle stores left, top, right, and bottom values.
    Coordinates are based on screen coordinates.
    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom
    set_points  -- reset rectangle coordinates
    contains  -- is a point inside?
    overlaps  -- does a rectangle overlap?
    top_left  -- get top-left corner
    bottom_right  -- get bottom-right corner
    expanded_by  -- grow (or shrink)
    """

    def __init__(self, pt1, pt2):
        """Initialize a rectangle from two points."""
        self.set_points(pt1, pt2)

    def set_points(self, pt1, pt2):
        """Reset the rectangle coordinates."""
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)

    def contains(self, pt):
        """Return true if a point is inside the rectangle."""
        x,y = pt.as_tuple()
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    def overlaps(self, other):
        """Return true if a rectangle overlaps this rectangle."""
        return (self.right > other.left and self.left < other.right and
                self.top < other.bottom and self.bottom > other.top)

    def top_left(self):
        """Return the top-left corner as a Point."""
        return Point(self.left, self.top)

    def bottom_right(self):
        """Return the bottom-right corner as a Point."""
        return Point(self.right, self.bottom)

    def expanded_by(self, n):
        """Return a rectangle with extended borders.
        Create a new rectangle that is wider and taller than the
        immediate one. All sides are extended by "n" points.
        """
        p1 = Point(self.left-n, self.top-n)
        p2 = Point(self.right+n, self.bottom+n)
        return Rect(p1, p2)

    def __str__( self ):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top, self.right,self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, Point(self.left, self.top), Point(self.right, self.bottom))

class Polygon:

    def __init__(self, pts=[]):
        """Initialize a polygon from list of points."""
        self.set_points(pts)
        self.set_direction("N")     #

    def set_points(self, pts):
        """Reset the poly coordinates."""

        self.minX = sys.maxsize
        self.minY = sys.maxsize
        self.maxX = sys.maxsize * -1
        self.maxY = sys.maxsize * -1

        self.points = []
        #self.mbr = Rect()
        for p in pts:
            x,y = p

            if x < self.minX:
                self.minX = x
            if x > self.maxX:
                self.maxX = x
            if y < self.minY:
                self.minY = y
            if y > self.maxY:
                self.maxY = y

            self.points.append(Point(x,y))

        self.mbr = Rect(Point(self.minX,self.minY),Point(self.maxX,self.maxY))

    def get_points(self):
        generic = []
        for p in self.points:
            generic.append(p.as_tuple())
        return generic




    # determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs.
    def point_inside_polygon(self, p):

        n = len(self.points)
        inside =False

        p1x,p1y = self.points[0].as_tuple()
        for i in range(n+1):
            p2x,p2y = self.points[i % n].as_tuple()
            if p.y > min(p1y,p2y):
                if p.y <= max(p1y,p2y):
                    if p.x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (p.y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or p.x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def set_direction(self,direction):
         assert direction in ['N','NE','E','SE','S','SW','W','NW']
         for p in self.points:
              p.set_direction(direction)
         self.direction = direction

    def get_direction(self):
       return self.direction

    def update_position(self):
        generic = []
        for p in self.points:
            p.update_position()
            generic.append(p.as_tuple())

        self.set_points(generic)

    def __str__( self ):
        return "<Polygon \n Points: %s \n Mbr: %s>" % ("".join(str(self.points)),str(self.mbr))

    def __repr__(self):
        return "%s %s" % (self.__class__.__name__,''.join(str(self.points)))


class Driver(pantograph.PantographHandler):

    def setup(self):

        self.poly1 = Polygon([(405, 528),(377, 567),(444, 613),(504, 584),(519, 507),(453, 448),(380, 450),(365, 478),(374, 525)])
        self.poly1.set_direction("NE")
        self.poly2 = Polygon([(83, 163),  (90, 74),  (145, 60),  (201, 69),  (265, 46),(333, 61),  (352, 99),  (370, 129),  (474, 138),  (474, 178),  (396, 225),(351, 275),  (376, 312),  (382, 356),  (338, 368),  (287, 302),  (224, 304), (128, 338),  (129, 270), (110, 316),  (83, 231),  (103, 201),  (126, 162),  (165, 151)])
        self.poly2.set_direction("E")
        self.poly3 = Polygon([(800,300),(750,450),(900,200),(950,250)])
        self.poly3.set_direction("N")
        self.p1 = Point(self.width/2, self.height/2)
        self.p2 = Point(100, 345)
        self.p3 = Point(543,743)
        self.p1.set_direction("SE")
        self.p2.set_direction("E")
        self.p3.set_direction("NW")
        self.polys=[self.poly1, self.poly2, self.poly3]
        self.pts=[self.p1,self.p2,self.p3]
    def drawShapes(self):
        self.draw_polygon(self.poly1.get_points() , color = "#F00")
        self.draw_polygon(self.poly2.get_points() , color = "#0F0")
        self.draw_polygon(self.poly3.get_points() , color = "#00F")
        self.draw_rect(0, 0, self.width, self.height, color= "#000")

        if  self.poly1.point_inside_polygon(self.p1):
            color1 = "#0F0"
        elif self.poly2.point_inside_polygon(self.p1):
            color1 = "#0F0"
        elif self.poly3.point_inside_polygon(self.p1):
            color1 = "#0F0"
        else:
            color1 = "#F00"
        self.fill_oval(self.p1.x, self.p1.y, 7, 7, color1)

        if  self.poly1.point_inside_polygon(self.p2):
            color2 = "#0F0"
        elif self.poly2.point_inside_polygon(self.p2):
            color2 = "#0F0"
        elif self.poly3.point_inside_polygon(self.p2):
            color2 = "#0F0"
        else:
            color2 = "#F00"
        self.fill_oval(self.p2.x, self.p2.y, 7, 7, color2)

        if  self.poly1.point_inside_polygon(self.p3):
            color3 = "#0F0"
        elif self.poly2.point_inside_polygon(self.p3):
            color3 = "#0F0"
        elif self.poly3.point_inside_polygon(self.p3):
            color3 = "#0F0"
        else:
            color3 = "#F00"
        self.fill_oval(self.p3.x, self.p3.y, 7, 7, color3)

    def changeDirection(self, p1, p2):
        #pass
        poly1points = p1.get_points()
        poly2points = p2.get_points()
        for point in poly1points:
            if p1.get_direction() == "N" and point[1] < self.height:
                p1.set_direction("S")
                return p1.get_direction()
            if p1.get_direction() == "NE" and point[1] < self.height:
                p1.set_direction("SE")
                return p1.get_direction()
            if p1.get_direction() == "NE" and point[0] > self.width:
                p1.set_direction("NW")
                return p1.get_direction()
            if p1.get_direction() == "E" and point[0] > self.width:
                p1.set_direction("W")
                return p1.get_direction()
            if p1.get_direction() == "SE" and point[1] > self.height:
                p1.set_direction("NE")
                return p1.get_direction()
            if p1.get_direction() == "SE" and point[0] > self.width:
                p1.set_direction("SW")
                return p1.get_direction()
            if p1.get_direction() == "S" and point[1] > self.height:
                p1.set_direction("N")
                return p1.get_direction()
            if p1.get_direction() == "SW" and point[1] > self.height:
                p1.set_direction("NW")
                return p1.get_direction()
            if p1.get_direction() == "SW" and point[0] < self.width:
                p1.set_direction("SE")
                return p1.get_direction()
            if p1.get_direction() == "W" and point[0] < self.width:
                p1.set_direction("E")
                return p1.get_direction()
            if p1.get_direction() == "NW" and point[1] < self.height:
                p1.set_direction("SW")
                return p1.get_direction()
            if p1.get_direction() == "NW" and point[0] < self.width:
                p1.set_direction("NE")
                return p1.get_direction()


    def hitWall(self, p):
        pass
        # if x>=self.width or y>= self.width:
        #     return True
        # return False

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)
        self.p1.update_position()
        self.p2.update_position()
        self.p3.update_position()

        self.poly1.update_position()
        self.poly2.update_position()
        self.poly3.update_position()
    
        self.drawShapes()


if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()
