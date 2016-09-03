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
#
# Member Functions:
# lightdir(self, i, j)
# Purpose: Returns normalized vector in tangent space to S3 at position. The vector comes from specifying i and j.
# Parameters: i is an integer such that 0 <= i < npoints. Controls horizontal movement in camera's vision.
#             j is an integer such that 0 <= j < npoints. Controls vertical movement in camera's vision.

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
		lightdirection = self.direction + (i/self.npoints - 0.5)*self.hoffset
		lightdirection = lightdirection + (j/self.npoints - 0.5)*self.voffset
		size = np.linalg.norm(lightdirection) 
		lightdirection = lightdirection / size
		return lightdirection


# Class for storing information of Ball in S3
# __init__ parameters:
#     center = The position of the center of the ball in S3. Must be a normalized unit vector.
#     radius = The Euclidean radius of the ball. That is the radius of the straight line distance in R4.

class Ball:
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius

# Class for storing functions related to calculating geometric quantities on S3.

class S3:
	def dist(self, x, y):
		dotproduct = 0
		for i in range(4):
			dotproduct += point1[i]*point2[i]
		return np.arccos(dotproduct)

# Function: findintersectball
# Purpose: Find the angle (in radians) of the intersection of a light ray starting at camera's position in a particular direction with a particular ball. If there is an intersection then the returned angle is between 0 and 2*np.pi.
# Parameters: cposition is a vector of the camera's current position.
#             ldirection is the direction of the light ray.
#             ball is the ball for detecting the intersection.

def findintersectball(cposition, ldirection, ball):
	bcenter = ball.center
	bradius = ball.radius
	failintersect = np.array([0.0, 0.0, 0.0, 0.0])
	failt = -1.0
	t = [0.0, 0.0]
	result = np.array([0.0, 0.0, 0.0, 0.0])
	prodcpos = 0.0
	prodcdir = 0.0
	for i in range(4):

		prodcpos += cposition[i]*bcenter[i]
		prodcdir += ldirection[i]*bcenter[i]

	magnitude = np.sqrt(prodcpos**2 + prodcdir**2)
	if magnitude == 0:

		return failt

	D = (1 - 0.5 * bradius**2) / magnitude
	if D**2 > 1.0: 

		return failt

	else:

		a = prodcpos/magnitude
		b = prodcdir/magnitude
		xcoord = D*a - np.sqrt(1-D**2)*b
		ycoord = D*b + np.sqrt(1-D**2)*a
		t[0] = np.arctan2(ycoord, xcoord)+np.pi

		xcoord = D*a + np.sqrt(1-D**2)*b
		ycoord = D*b - np.sqrt(1-D**2)*a
		t[1] = np.arctan2(ycoord, xcoord)+np.pi
		if t[0] < t[1]:
			truet = t[0]
		else:
			truet = t[1]
		return truet 
