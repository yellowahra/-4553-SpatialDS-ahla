"""
@author - Ahla CHO
@date- 10/19/2015
@description - This program uses a quadtree for collision detection of an n number of balls.
The balls are changed color, grow in size, and change direction when they collide. Uses python 2.7. Requires pantograph and numpy installed. After running copy go to the localhost by placing
http://127.0.0.1:8080/ in the browser in order to view the animation. The quadtree bounding boxes are shown behind the balls
as well to see it splitting in real time.
@resources - Help from at http://www.learnpygame.com, http://stackoverflow.com, http://gamedev.stackexchange.com/
"""
import sys
import math
import random
import pantograph
import numpy as np
import time

class Point(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    """
    @returns Point(x1+x2, y1+y2)
    """
    def __add__(self, p):
		return Point(self.x + p.x, self.y + p.y)
    """
    @returns Point(x1-x2, y1-y2)
    """
    def __sub__(self, p):
		return Point(self.x - p.x, self.y - p.y)
    """
    Point(x1*x2, y1*y2)
    """
    def __mul__(self, scalar):
		return Point(self.x * scalar, self.y * scalar)
    """
    Point(x1/x2, y1/y2)
    """
    def __div__(self, scalar):
		return Point(self.x / scalar, self.y / scalar)

    def __str__(self):
		return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    """
    Calculate the distance between two points.
    @returns distance
    """
    def distance_to(self, p):
        return (self - p).length()

    """
    @returns a tuple (x, y)
    """
    def as_tuple(self):
        return (self.x, self.y)

    """
    Return a full copy of this point.
    """
    def clone(self):
        return Point(self.x, self.y)

    """
    Convert co-ordinate values to integers.
    @returns Point(int(x),int(y))
    """
    def integerize(self):
        self.x = int(self.x)
        self.y = int(self.y)

    """
    Convert co-ordinate values to floats.
    @returns Point(float(x),float(y))
    """
    def floatize(self):
        self.x = float(self.x)
        self.y = float(self.y)

    """
    Moves / sets point to x,y .
    """
    def move_to(self, x, y):
        self.x = x
        self.y = y

    """
    Move to new (x+dx,y+dy).
    """
    def slide(self, p):
        self.x = self.x + p.x
        self.y = self.y + p.y

    """
    Move to new (x+dx,y+dy).
    """
    def slide_xy(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    """
    Rotate counter-clockwise by rad radians.
    Positive y goes *up,* as in traditional mathematics.
    Interestingly, you can use this in y-down computer graphics, if
    you just remember that it turns clockwise, rather than
    counter-clockwise.
    The new position is returned as a new Point.
    """
    def rotate(self, rad):
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
        return Point(x,y)

    """
    Rotate counter-clockwise around a point, by theta degrees.
    Positive y goes *up,* as in traditional mathematics.
    The new position is returned as a new Point.
    """
    def rotate_about(self, p, theta):

        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
        result.slide(p.x, p.y)
        return result

"""
Class Rect:
    A rectangle identified by two points.
    The rectangle stores left, top, right, and bottom values.
    Coordinates are based on screen coordinates.
    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom
@method: set_points     -- reset rectangle coordinates
@method: contains       -- is a point inside?
@method: overlaps       -- does a rectangle overlap?
@method: top_left       -- get top-left corner
@method: bottom_right   -- get bottom-right corner
@method: expanded_by    -- grow (or shrink)
source: https://wiki.python.org/moin/PointsAndRectangles
"""
class Rectangle:
    """
    Initialize a rectangle from two points.
    """
    def __init__ (self, pt1, pt2):
        self.set_points(pt1, pt2)

    """
    @fuction set_points
    description: dimensions of the rectangle by the given points
    """
    """
    Reset the rectangle coordinates.
    """
    def set_points(self, pt1, pt2):
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)
        self.width=self.right-self.left
        self.height=self.bottom- self.top

    """
    @function contains
    description: if a point is inside the rectangle, return true
    """

    def contains(self, pt):
        return (self.top_left().x <= pt.x and pt.x <= self.bottom_right() and
                self.top_left().y <= pt.y and pt.y<= self.bottom_right().y)
    """
    @function encompasses
    description: if rectangle is inside this rectangle, return true
    """
    def encompasses(self, other):
        return  (self.left <= other.left and self.right >= other.right and
                self.top <= other.top and self.bottom >= other.bottom)
    """
    @function overlaps
    description: if a rectangle overlpas this rectangle, returns true
    """
    def overlaps(self, other):
        return (self.right > other.left and self.left < other.right and
                self.top < other.bottom and self.bottom > other.top)

    """
    @function top_left
    description: retuns top-left point of rectangle
    """
    def top_left(self):
        return Point(self.left, self.top)

    """
    @function top_right
    descripton: returns top-right point of rectangle
    """
    def top_right(self):
        return Point(self.right, self.top)


    """
    @function bottom_left
    description: returns bottom-left point of rectangle
    """
    def bottom_left(self):
        return Point(self.left, self.bottom)
    """
    @function bottom_right
    description: returns bottom-right point of rectangle
    """
    def bottom_right(self):
        return Point(self.right, self.bottom)


    """
    @function expanded_by
    description:  Return a rectangle with extended borders.
    Create a new rectangle that is wider and taller than the
    immediate one. All sides are extended by "n" points.
    """
    def expanded_by(self, n):
        p1 = Point(self.left-n, self.top-n)
        p2 = Point(self.right+n, self.bottom+n)
        return Rect(p1, p2)

    """
    @function get_centroid
    description: get centroid of rectangle and return the cnetroid
    http://stackoverflow.com/questions/24478349/how-to-find-the-centroid-of-
    multiple-rectangles
    """
    def get_centroid(self):
		tempX = (self.left + self.width) / 2
		tempY = (self.top + self.height) / 2
		return Point(tempX, tempY)
    """
    @function get_side_collision
    description: which side of bounding box was hit
    http://gamedev.stackexchange.com/questions/24078/which-side-was-hit
    """
    def get_collision_side(self, other):
        wy = (self.width + other.width) * (self.get_centroid().y - other.get_centroid().y)
        hx = (self.height + other.height) * (self.get_centroid().x - other.get_centroid().x)
        if wy > hx:
            if wy > -hx:
                return "Top"
            else:
                return "Left"
        else:
            if wy > -hx:
                return "Right"
            else:
                return "Bottom"

    def __str__( self ):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top,self.right,self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,Point(self.left, self.top),Point(self.right, self.bottom))

class PointQuadTree(object):
    def __init__(self, bbox, maxPoints, points=[], level=0, maxLevel=4):
        self.northEast = None
        self.southEast = None
        self.southWest = None
        self.northWest = None

        self.points = points
        self.bbox = bbox
        self.maxPoints = maxPoints
        self.level = level
        self.maxLevel = maxLevel

    def __str__(self):
        return "\nnorthwest: %s,\nnorthEast: %s,\nsouthWest: %s,\nsouthEast: %s,\npoints: %s,\nbbox: %s,\nmaxPoints: %s,\nparent: %s" % (self.northWest, self.northEast,self.southWest, self.southEast,self.points,self.bbox,self.maxPoints,self.level)


	"""
	@function update
	Subdivides the nodes, puts the points into the right node, recursively updates each subtree, and checks for collisions in appropriate nodes and handles them
	"""
	def update(self):
		if len(self.points) >= self.maxPoints and self.level <= self.maxLevel:
			self.subdivide()
			self.subdividePoints()
			self.northEast.update()
			self.southEast.update()
			self.southWest.update()
			self.northWest.update()
		else:
			self.checkCollisionsPoints()

	"""
	@function subdivide
	Split this QuadTree node into four quadrants for NW/NE/SE/SW
	Modified from quadtree code pushed onto github
	"""
	def subdivide(self):
		left = self.bbox.left
		right = self.bbox.right
		top = self.bbox.top
		bottom = self.bbox.bottom
		midX = (self.bbox.width) / 2
		midY = (self.bbox.height) / 2
		self.northEast = PointQuadTree(Rectangle(Point(left + midX, top), Point(right, top + midY)), self.maxPoints, [], self.level + 1)
		self.northWest = PointQuadTree(Rectangle(Point(left, top), Point(left + midX,top + midY)), self.maxPoints, [], self.level + 1)
		self.southWest = PointQuadTree(Rectangle(Point(left, top + midY), Point(left + midX, bottom)), self.maxPoints, [], self.level + 1)
		self.southEast = PointQuadTree(Rectangle(Point(left + midX, top + midY), Point(right, bottom)), self.maxPoints, [], self.level + 1)

	"""
	@function subdividePoints
	description: Puts points in the quadtree into the leaf
	Found help at http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html
	"""
	def subdividePoints(self):
		for point in self.points:
			if self.northEast.bbox.overlaps(point.getBBox()) or self.northEast.bbox.encompasses(point.getBBox()):
				self.northEast.addPoint(point)
			if self.northWest.bbox.overlaps(point.getBBox()) or self.northWest.bbox.encompasses(point.getBBox()):
				self.northWest.addPoint(point)
			if self.southWest.bbox.overlaps(point.getBBox()) or self.southWest.bbox.encompasses(point.getBBox()):
				self.southWest.addPoint(point)
			if self.southEast.bbox.overlaps(point.getBBox()) or self.southEast.bbox.encompasses(point.getBBox()):
				self.southEast.addPoint(point)

	"""
	@function searchBox
	Return an array of all points within this QuadTree and its child nodes that fall
	within the specified bounding box
	Taken from quadtree implementation on github
	"""
	def searchBox(self, bbox):
		results = []

		if self.bbox.overlaps(bbox) or self.bbox.encompasses(bbox):
			# Test each point that falls within the current QuadTree node
			for p in self.points:
				# Test each point stored in this QuadTree node in turn, adding
				# to the results array
				#    if it falls within the bounding box
				if self.bbox.contains(p):
					results.append((bbox, self.level))

			# If we have child QuadTree nodes....
			if (not self.northWest == None):
				# ...  search each child node in turn, merging with any
				# existing results
				results = results + self.northEast.searchBox(self.bbox)
				results = results + self.northWest.searchBox(self.bbox)
				results = results + self.southWest.searchBox(self.bbox)
				results = results + self.southEast.searchBox(self.bbox)

		return results

	"""
	@function searchNeighbors
	Returns the containers points that are in the same container as another point
	Taken from quadtree implementation on github
	"""
	def searchNeighbors(self, point):
		#If its not a point (its a bounding rectangle)
		if not hasattr(point, 'x'):
			return []

		results = []

		if self.bbox.containsPoint(point):
			# Test each point that falls within the current QuadTree node
			for p in self.points:
				# Test each point stored in this QuadTree node in turn, adding
				# to the results array
				#    if it falls within the bounding box
				if self.bbox.containsPoint(p):
					results.append(p)


			# If we have child QuadTree nodes....
			if (not self.northWest == None):
				# ...  search each child node in turn, merging with any
				# existing results
				results = results + self.northEast.searchNeighbors(point)
				results = results + self.northWest.searchNeighbors(point)
				results = results + self.southWest.searchNeighbors(point)
				results = results + self.southEast.searchNeighbors(point)

		return results

	"""
	@function getBBoxes
	Gets all of the bounding boxes of the quadtree
	Taken from quadtree implementation on github
	"""
	def getBBoxes(self):
		bboxes = []

		bboxes.append(self.bbox)

		if (not self.northWest == None):
			# ...  search each child node in turn, merging with any existing
			# results
			bboxes = bboxes + self.northEast.getBBoxes()
			bboxes = bboxes + self.northWest.getBBoxes()
			bboxes = bboxes + self.southWest.getBBoxes()
			bboxes = bboxes + self.southEast.getBBoxes()

		return bboxes

	"""
	@function checkCollisionsPoints
	description: Checks all the points in the current quadtree node for collisions then handles the collision
    http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html
	"""
	def checkCollisionsPoints(self):
		for i, particle in enumerate(self.points):
			for particle2 in self.points[i + 1:]:
				if (particle.collides(particle2)):
					particle.handleCollision(particle2)


	"""
	@function addPoint
	description: Adds a point to the quadtree
	http://www.learnpygame.com/2015/03/implementing-quadtree-collision-system.html
	"""
	def addPoint(self, point):
		self.points.append(point)

class Vector (object):

    def __init__ (self, p1, p2):
        assert not p1 == None
        assert not p2 == None
        self.p1=p1
        self.p2=p2
        self.v=[self.p1x - self.p2.x, self.p1.y - self.p2.y]
        self.a, self.b = self.v

    def __str__ (self):
        return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\n b: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)

    def __repr__ (self):
        return "[\n p1: %s,\n p2: %s,\n vector: %s,\n a: %s,\n b: %s\n]" % (self.p1, self.p2, self.v,self.a,self.b)

class VectorOps(object):

	def __init__(self,p1=None, p2=None, velocity=1):
		self.p1 = p1
		self.p2 = p2
		self.dx = 0
		self.dy = 0
		if not self.p1 == None and not self.p2 == None:
			self.v = Vector(p1,p2)
			self.velocity = velocity
			self.magnitude = self._magnitude()
			self.bearing = self._bearing()
			self.step = self._step()
		else:
			self.v = None
			self.velocity = None
			self.bearing = None
			self.magnitude = None


	def _bearing(self):
		dx = self.p2.x - self.p1.x
		dy = self.p2.y - self.p1.y
		rads = math.atan2(-dy,dx)
		return rads % 2 * math.pi         # In radians
		#degs = degrees(rads)

	def _magnitude(self):
		assert not self.v == None
		return math.sqrt((self.v.a ** 2) + (self.v.b ** 2))


	def _step(self):
		cosa = math.sin(self.bearing)
		cosb = math.cos(self.bearing)
		self.dx = cosa * self.velocity
		self.dy = cosb * self.velocity
		return [cosa * self.velocity, cosb * self.velocity]


	def __str__(self):
		return "[\n Vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s,\n step: %s]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)

	def __repr__(self):
		return "[\n Vector: %s,\n velocity: %s,\n bearing: %s,\n magnitude: %s,\n step: %s]" % (self.v, self.velocity, self.bearing,self.magnitude,self.step)

	def handleCollision(self, ball):
		xDist = self.center.x - ball.center.x #calculate x distance between the ball centers
		yDist = self.center.y - ball.center.y #calculate y distance between the ball centers
		distSquared = xDist * xDist + yDist * yDist #find the squared distance between the ball centers
		xVel = ball.vectorOps.dx - self.vectorOps.dx #find the combined x velocity of the balls
		yVel = ball.vectorOps.dy - self.vectorOps.dy #find the combined y velocity of the balls
		dotProduct = xDist * xVel + yDist * yVel #determine the dot product to determine the direction the balls are moving
		if(dotProduct > 0): #if the balls are moving toward each other
			collisionScale = dotProduct / distSquared #The Collision vector is the speed difference projected on the Dist vector,
			xCollision = xDist * collisionScale #thus it is the component of the speed difference needed for the collision.
			yCollision = yDist * collisionScale
			combinedMass = self.mass + ball.mass
			collisionWeightA = 2 * ball.mass / combinedMass #figure out the weight of each ball in the collision
			collisionWeightB = 2 * self.mass / combinedMass
			self.vectorOps.dx += collisionWeightA * xCollision #change the x and y velocity of the balls according to the collision
			self.vectorOps.dy += collisionWeightA * yCollision
			ball.vectorOps.dx -= collisionWeightB * xCollision
			ball.vectorOps.dy -= collisionWeightB * yCollision
			if(self.radius < self.maxRadius): #If you haven't reached the maximum size of the circle increase its radius
									 #after a collision
				self.radius += .5
			if(ball.radius < ball.maxRadius):
				ball.radius += .5
			self.colorIndex = (self.colorIndex + 1) % len(self.colorList) #increment the color index to get the next color
			ball.colorIndex = (ball.colorIndex + 1) % len(ball.colorList)
			self.color = self.colorList[self.colorIndex] #update the color
			ball.color = ball.colorList[ball.colorIndex]
		self.move() #move the ball to get out of the collision, moves even if the circles aren't
			  #moving toward each other so they don't get stuck
		ball.move()

	def as_tuple(self):
		return (self.x, self.y)


	def _str__(self):
		return "[\n center: %s,\n radius: %s,\n Vector: %s,\n speed: %s\n ]" % (self.center,self.radius, self.vectorOps, self.velocity)

	def __repr__(self):
		return "[\n center: %s,\n radius: %s,\n Vector: %s,\n speed: %s\n ]" % (self.center, self.radius, self.vectorOps, self.velocity)


class Bounds(object):

	def __init__(self,minx,miny,maxx,maxy):
		self.minX = minx
		self.minY = miny
		self.maxX = maxx
		self.maxY = maxy

	def __repr__(self):
		return "[%s %s %s %s]" % (self.minX, self.minY, self.maxX,self.maxY)

class Driver(pantograph.PantographHandler):

	def setup(self):
		self.bounds = Bounds(0,0,self.width,self.height)
		self.bbox = Rectangle(Point(0, 0), Point(10, 10))
		self.ballSpeeds = np.arange(1,4,1)
		self.ballMasses = np.arange(1,10,1)
		self.numBalls = 50
		self.ballSize = 10
		self.radius = self.ballSize / 2
		self.balls = []
		self.boxes = []
		self.freeze = False
		self.colorList = []
		self.maxBallRadius = (self.width + self.height) / self.numBalls
		mass = random.choice(self.ballMasses)
		for i in xrange(0, 16):
			for j in xrange(0, 16):
				for k in xrange(0, 16):
					self.colorList.append("#" + "{0:x}{1:x}{2:x}".format(i,j,k))
		for i in range(self.numBalls):
			speed = random.choice(self.ballSpeeds)
			newBall = Ball(self.getRandomPosition(),self.ballSize, self.bounds, self.colorList, speed, mass, self.maxBallRadius)
			self.balls.append(newBall)


		self.qt = PointQuadTree(Rectangle(Point(0,0),Point(self.width,self.height)),2, self.balls)


	def update(self):
		if not self.freeze:
			self.moveBalls()
		self.clear_rect(0, 0, self.width, self.height)
		self.drawBalls()
		self.drawBoxes()

	def getRandomPosition(self):
		x = random.randint(0 + self.ballSize, int(self.width) - self.ballSize)
		y = random.randint(0 + self.ballSize, int(self.height) - self.ballSize)
		return Point(x,y)


	def drawBoxes(self):
		boxes = self.qt.getBBoxes()
		for box in boxes:
			self.draw_rect(box.top_left().x, box.top_left().y, box.width, box.height)
		#for r in self.balls:
			#self.draw_rect(r.getBBox().top_left().x, r.getBBox().top_left().y,
			#r.getBBox().width, r.getBBox().height)


	def drawBalls(self):
		for r in self.balls:
			self.fill_circle(r.x, r.y, r.radius, r.color)


	def moveBalls(self):
		for ball in self.balls:
			ball.move()
		self.qt = PointQuadTree(Rectangle(Point(0, 0),Point(self.width, self.height)), 2, self.balls)
		self.qt.update()


	def on_click(self,InputEvent):
		if self.freeze == False:
			self.freeze = True
		else:
			self.freeze = False


	def on_key_down(self,InputEvent):
		# User hits the UP arrow
		if InputEvent.key_code == 38:
			for r in self.balls:
				r.changeSpeed(r.velocity * 1.25)
		# User hits the DOWN arrow
		if InputEvent.key_code == 40:
			for r in self.balls:
				r.changeSpeed(r.velocity * .75)
			pass


if __name__ == '__main__':
	app = pantograph.SimplePantographApplication(Driver)
	app.run()
