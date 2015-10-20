"""
@author - AHLA CHO
@date -  10/05/2015
@description - THREE POLYGONES AND THREE POINTS ARE MOVING
            AND IF POINTS ARE IN THE POLYGONES, THEY ARE CHANGED COLOR
            AND IF POLYGONES ARE COLLISION, THEY ARE CHANGE THE DIRECTION
"""
import pantograph
import math
import sys
import copy

"""
Point and Rectangle classes.
This code is in the public domain.
Point  -- point with (x,y) coordinates
Rect  -- two points, forming a rectangle
"""
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

    def update_position(self):
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
    """A polygon contains a sequence of points on the 2D plane
    and connects them togother.
    """

    def __init__(self, pts=[]):
        """Initialize a polygon from list of points."""
        self.set_points(pts)

    def set_points(self, pts):
        """Reset the poly coordinates."""

        self.minX = sys.maxsize
        self.minY = sys.maxsize
        self.maxX = sys.maxsize * -1
        self.maxY = sys.maxsize * -1

        self.points = []

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

    """
    @function get_points
    Return a sequence of tuple of the points of the pology.

    """
    def get_points(self):
        generic = []
        for p in self.points:
            generic.append(p.as_tuple())
        return generic

    """
    @function
    determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs.
    """
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

    def is_collision(self, poly):
        """Check if two pologies collide with each other by examing if their mbrs overlap."""
        return self.mbr.overlaps(poly.mbr) or poly.mbr.overlaps(self.mbr)

    def set_direction(self, direction):
        """Set direction for all points of the pology."""
        for p in self.points:
            p.set_direction(direction)

    def update_position(self):
        """Update positions of all points of the pology, and the mbr."""
        px, py = self.points[0].x, self.points[0].y
        for p in self.points:
            p.update_position()
        dx, dy = self.points[0].x - px, self.points[0].y - py

        # update mbr
        mbr = self.mbr
        mbr.left += dx
        mbr.right += dx
        mbr.top += dy
        mbr.bottom += dy

    def __str__( self ):
        return "<Polygon \n Points: %s \n Mbr: %s>" % ("".join(str(self.points)),str(self.mbr))

    def __repr__(self):
        return "%s %s" % (self.__class__.__name__,''.join(str(self.points)))

class Driver(pantograph.PantographHandler):
    def setup(self):
        """Set up the points, color, directions....
        """
        self.p1 = Point(300, 100)
        self.p2 = Point(self.width/2, self.height/2)
        self.p3 = Point(700, 200)
        self.p1.set_direction("SE")
        self.p2.set_direction("N")
        self.p3.set_direction("NW")
        self.p1.color = "#0F0"
        self.p2.color = "#0F0"
        self.p3.color = "#0F0"

        self.poly1 = Polygon([(405, 367),(444, 413),(504, 384),(519, 307),(453, 248),(380, 250),(365, 278),(374, 325)])
        self.poly2 = Polygon([(80,163),(90, 74),(145,60),(210,69)])
        self.poly3 = Polygon([(236,144),  (317,179), (323,229), (187,299), (150,280)])
        self.poly1.set_direction("SE")
        self.poly2.set_direction("NE")
        self.poly3.set_direction("SW")

    def drawShapes(self):
        """Draw points and polygons on the canvas."""

        self.draw_rect(0, 0, self.width, self.height, color= "#000")
        self.draw_polygon(self.poly2.get_points(), color = "#000")
        self.draw_polygon(self.poly1.get_points(), color = "#000")
        self.draw_polygon(self.poly3.get_points(), color = "#000")

        self.fill_oval(self.p1.x, self.p1.y, 5, 5, self.p1.color)
        self.fill_oval(self.p2.x, self.p2.y, 5, 5, self.p2.color)
        self.fill_oval(self.p3.x, self.p3.y, 5, 5, self.p3.color)

    """
    @function hitWall
    Check points or polygons hit a wall. then if yes, change their directions.
    """
    def hitWall(self):
        for p in [self.p1, self.p2, self.p3]:
            axis = self.__point_hit_wall(p)
            if axis:
                p.set_direction(self.__reflection_direction(p.direction, axis))
        for poly in [self.poly1, self.poly2, self.poly3]:
            for p in poly.points:
                axis = self.__point_hit_wall(p)
                if axis:
                    poly.set_direction(self.__reflection_direction(p.direction, axis))
                    break

    """
    @function __point_hit_wall
    Check if a point hit the wall.
    """
    def __point_hit_wall(self, p):
        axis = None
        if p.x >= self.width or p.x <= 0:
            axis = 'y'
        if p.y >= self.height or p.y <= 0:
            axis = 'x'
        return axis
    """
    @function __reflection_direction
    Reflect the moving direction after hit a wall.
    """
    def __reflection_direction(self, direction, axis):
        return {'E':'W', 'W':'E', 'S':'N', 'N':'S', 'NW':'SW' if axis == 'x' else 'NE', 'NE':'SE' if axis == 'x' else 'NW',\
                'SW':'NW' if axis == 'x' else 'SE', 'SE':'NE' if axis == 'x' else 'SW' }[direction]

    """
    @function pointsInPolygon
    Check if some of the three points are in one of the three polygones.
    If yes, change color of the point.
    """
    def pointsInPolygon(self):
        for p in [self.p1, self.p2, self.p3]:
            for poly in [self.poly1, self.poly2, self.poly3]:
                if poly.point_inside_polygon(p):
                    p.color = "#F00"
                    break
                else:
                    p.color = "#0F0"
    """
    @function polygonCollide
    Check if one of the three polygons collides with another.
    reverse their directions.
    """
    def polygonCollide(self, prepoly1, prepoly2, prepoly3):

        if self.poly1.is_collision(self.poly2) and not prepoly1.is_collision(prepoly2):
            print('collision 1 2')
            self.poly1.set_direction(self.__reverse_direction(self.poly1.points[0].direction))
            self.poly2.set_direction(self.__reverse_direction(self.poly2.points[0].direction))
        elif self.poly1.is_collision(self.poly3) and not prepoly1.is_collision(prepoly3):
            print('collision 1 3')
            self.poly1.set_direction(self.__reverse_direction(self.poly1.points[0].direction))
            self.poly3.set_direction(self.__reverse_direction(self.poly3.points[0].direction))
        elif self.poly3.is_collision(self.poly2) and not prepoly3.is_collision(prepoly2):
            print('collision 3 2')
            self.poly3.set_direction(self.__reverse_direction(self.poly3.points[0].direction))
            self.poly2.set_direction(self.__reverse_direction(self.poly2.points[0].direction))

    """
    @function __reverse_direction
    Reverse the direction after collision.
    """
    def __reverse_direction(self, direction):
        return {'E':'W', 'W':'E', 'S':'N', 'N':'S', 'NW':'SE', 'NE':'SW', 'SE':'NW', 'SW':'NE'}[direction]

    """
    @function update
    Update points and polygones after a interval, such as position, direction and color.
    """
    def update(self):
        self.clear_rect(0, 0, self.width, self.height) # remove entire previous draw

        self.p1.update_position()
        self.p2.update_position()
        self.p3.update_position()

        prepoy1, prepoly2, prepoly3 = copy.polycopy(self.poly1), copy.polycopy(self.poly2), copy.polycopy(self.poly3)

        for poly in [self.poly1, self.poly2, self.poly3]:
            poly.update_position()

        self.pointsInPolygon()
        self.polygonCollide(prepoly1, prepoly2, prepoly3)
        self.hitWall()
        self.drawShapes()

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()
