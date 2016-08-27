import numpy as np
import matplotlib.pyplot as plt
import pylab
import time

# This is a class for storing information on the camera.
# __init__ parameters:
#     position = The position of the camera in S3. Must be a normalized unit vector.
#     direction = The direction of the camera in S3. Must be a normalized unit vector that
#            is orthogonal to position.
#     horizontaldir = The direction that corresponds to horizontal motion on screen. Must be a normalized unit vector.
#           Should be orthogonal to position.
#     verticaldir = The direction that corresponds to vertical motion on screen. Must be a normalized unit vector.
#           Should be orthogonal to position.
#     viewangle = Angle in radians that camera can see in the horizontal and vertical directions.
#     npoints = Number of points to process in horizontal direction and also in vertical direction. So
#          to process the camera's view, npoints**2 points will be processed.

class Camera:
	def __init__(self, position, direction, horizontaldir, verticaldir, viewangle, npoints):
		self.position = position
		self.direction = direction
		self.horizontaldir = horizontaldir
		self.verticaldir = verticaldir
		self.viewangle = viewangle
		self.lengthdifference = np.tan(viewangle/2.0)
		self.hoffset = self.lengthdifference*horizontaldir 
		self.voffset = self.lengthdifference*verticaldir 
		self.npoints = npoints

	def lightdir(self, i, j):
		self.lightdirection = self.direction + (i/self.npoints - 0.5)*self.hoffset
		self.lightdirection = self.lightdirection + (j/self.npoints - 0.5)*self.voffset
		self.size = np.linalg.norm(self.lightdirection) 
		self.lightdirection = self.lightdirection / self.size
		return self.lightdirection


# Class for storing information of Ball in S3
# __init__ parameters:
#     center = The position of the center of the ball in S3. Must be a normalized unit vector.
#     radius = The Euclidean radius of the ball. That is the radius of the straight line distance in R4.

class Ball:
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius

ballradii = np.array([0.4, 0.9, 0.2])
ballcenters = np.array([[0, 0, 0, 1.0]
	               ,[0, 0, 1.0, 0]
		       ,[0, np.sin(0.15*np.pi), 0, np.cos(0.15*np.pi)]])

nspheres = len(ballradii)

camposition = np.array([1.0, 0, 0, 0])
camdirection = np.array([0, 0, 0, 1.0])
hdirection = np.array([0, 1.0, 0, 0])
vdirection = np.array([0, 0, 1.0, 0])
viewangle = np.pi / 4 * 3
npoints = 200
mycam = Camera(camposition, camdirection, hdirection, vdirection, viewangle, npoints)

visualpoints = [[0 for x in range(npoints)] for y in range(npoints)] 

maxangle = 2*np.pi
dangle = 2*np.pi/30 
nangle = (int) (maxangle / dangle)
failcolor = 0.0 

def ballcolormap( i, position):
	diff = np.array([0.0, 0.0, 0.0, 0.0])
	myresultwhat = 0.0
	diff = position - ballcenters[i]
	if i==0:

		myresultwhat = 0.3+0.2*np.sin(diff[1]/ballradii[i]*2*np.pi)

	elif i==1:

		myresultwhat = 0.8+0.2*np.sin(diff[1]/ballradii[i]*np.pi)

	elif i==2:

		myresultwhat = 0.6 + 0.1*np.sin(diff[2]/ballradii[i]*2*np.pi)
		myresultwhat += 0.1*np.sin(diff[3]/ballradii[i]*3*np.pi)
	else:
		myresultwhat = 1.0

	if myresultwhat < 0.0:
		myresultwhat = 0.0

	return myresultwhat 

def lightdir( i, j):
	newdirection = camdirection + (i/nvisualpoints - 0.5)*camoffsetx
	newdirection = newdirection + (j/nvisualpoints - 0.5)*camoffsety
	size = np.linalg.norm(newdirection) 
	newdirection = newdirection / size
	return newdirection

def colordirection( ldirection , lowbounddist):
	position = camposition.copy()
	angle = lowbounddist 
	color = failcolor
	while angle < maxangle and color==failcolor:	
		position = np.cos(angle)*camposition
		position += np.sin(angle)*ldirection
		for j in range(len(ballcenters)):
			if ( np.linalg.norm(position - ballcenters[j]) < ballradii[j]):
				color = ballcolormap(j, position)
		angle += dangle
	return color

def spheredist(point1, point2):
	dotproduct = 0
	for i in range(4):
		dotproduct += point1[i]*point2[i]
	return np.arccos(dotproduct)

def findlowbounddist(point):
	lowbound = 2*np.pi
	for i in range(len(ballcenters)):
		current = spheredist(point, ballcenters[i])
		current -= ballradii[i]
		if current < lowbound:
			lowbound = current
	if lowbound < 0:
		lowbound = 0
	return lowbound

def solvecirclepoint(xcoord, ycoord):
	if xcoord == 0 and ycoord > 0:
		t = np.pi*0.5
	elif xcoord == 0 and ycoord <= 0:
		t = np.pi*1.5
	else:
		t = np.arctan(ycoord/xcoord)
		if t >= 0 and xcoord < 0:
			t = np.pi + t
		elif t < 0 and xcoord > 0:
			t = 2*np.pi + t
		elif t < 0 and xcoord < 0:
			t = np.pi + t
	return t


def findintersectball(cposition, ldirection, bcenter, bradius):
	failintersect = np.array([0.0, 0.0, 0.0, 0.0])
	failt = -1.0
	t = [0.0, 0.0]
	result = np.array([0.0, 0.0, 0.0, 0.0])
	prodcpos = 0
	prodcdir = 0
	for i in range(4):

		prodcpos += cposition[i]*bcenter[i]
		prodcdir += ldirection[i]*bcenter[i]

	magnitude = np.sqrt(prodcpos**2 + prodcdir**2)
	if magnitude == 0:

		return failt

	D = (1 - 0.5 * bradius**2) / magnitude
	if D**2 > 1: 

		return failt

	else:

		a = prodcpos/magnitude
		b = prodcdir/magnitude
		xcoord = D*a - np.sqrt(1-D**2)*b
		ycoord = D*b + np.sqrt(1-D**2)*a
		t[0] = solvecirclepoint(xcoord, ycoord)	

		xcoord = D*a + np.sqrt(1-D**2)*b
		ycoord = D*b - np.sqrt(1-D**2)*a
		t[1] = solvecirclepoint(xcoord, ycoord)
		if t[0] < t[1]:
			truet = t[0]
		else:
			truet = t[1]
		return truet 

	
starttime = time.time()
for i in range(npoints):
	lowbound = findlowbounddist(camposition)
	for j in range(npoints):
		minintersectangle = -1.0
		intersectsphere = -1
		currentlight = mycam.lightdir(i,j)
		for k in range(len(ballcenters)):
			newangle = findintersectball( mycam.position, currentlight, ballcenters[k], ballradii[k])
			if newangle > 0 and (newangle < minintersectangle or minintersectangle < 0):
				minintersectangle = newangle
				intersectsphere = k
		if minintersectangle >= 0:
			intersect = np.cos(minintersectangle)*mycam.position + np.sin(minintersectangle)*currentlight
			visualpoints[i][j] = ballcolormap(intersectsphere, intersect)
		else:
			visualpoints[i][j] = failcolor
		#visualpoints[i][j] = colordirection( lightdir(i,j), lowbound)
	if (i % (int(npoints/10)) == 0):
		print("Finished processing visualpoints["+str(i)+"][:]")
endtime = time.time()
print ("Time to finish is %s seconds" % (endtime - starttime))
		
xmesh, ymesh = np.meshgrid(np.array(range(npoints)),np.array(range(npoints))) 

plt.pcolor(xmesh, ymesh, visualpoints, cmap = 'CMRmap')# vmin = 0.0, vmaz = 1.0)
plt.show()

