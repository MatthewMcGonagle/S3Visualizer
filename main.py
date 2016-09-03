from S3Visualizer import *

# Initialize an array listing the radii of the different balls.

ballradii = np.array([0.4, 0.9, 0.2, 0.2])

# Initialize an array listing the positions of the centers of the different balls.

ballcenters = np.array([[0, 0, 0, 1.0]
	               ,[0, 0, 1.0, 0]
		       ,[0, np.sin(0.15*np.pi), 0, np.cos(0.15*np.pi)]
		       ,[0, 0, np.sin(0.15*np.pi), np.cos(0.15*np.pi)]])

# Construct an array of balls using ballradii and ballcenters

listofballs = [Ball(ballcenters[i], ballradii[i]) for i in range(len(ballradii)) ]

# Variable to store number of spheres.

nspheres = len(listofballs)

# Variables to set up camera, followed by camera initialization.

camposition = np.array([1.0, 0, 0, 0])
camdirection = np.array([0, 0, 0, 1.0])
hdirection = np.array([0, 1.0, 0, 0])
vdirection = np.array([0, 0, 1.0, 0])
viewangle = np.pi / 4 * 3
npoints = 200
mycam = Camera(camposition, camdirection, hdirection, vdirection, viewangle, npoints)

# Two-dimensional array for holding color grid of camera's vision. This will be the array that
# is finally printed out after computing the camera's vision.

visualpoints = [[0 for x in range(npoints)] for y in range(npoints)] 

# The color to print if there is no interesect found. Default to black = 0.0

failcolor = 0.0

# Function: ballcolormap
# Purpose: Function to determine the colors at different positions on the ball.
# Parameters: i is an integer such that 0 <= i < nspheres.
#             position is a vector giving a position on ball i that is used to determine the color.

def ballcolormap( i, position):
	diff = np.array([0.0, 0.0, 0.0, 0.0])
	colorresult = 0.0
	diff = position - ballcenters[i]
	if i==0:

		colorresult = 0.3+0.2*np.sin(diff[1]/ballradii[i]*2*np.pi)

	elif i==1:

		colorresult = 0.8+0.2*np.sin(diff[1]/ballradii[i]*np.pi)

	elif i==2:

		colorresult = 0.6 + 0.1*np.sin(diff[2]/ballradii[i]*2*np.pi)
		colorresult += 0.1*np.sin(diff[3]/ballradii[i]*3*np.pi)

	elif i==3:

		colorresult = 0.3 + 0.1*np.sin(diff[2]/ballradii[i]*2*np.pi)
		colorresult += 0.1*np.sin(diff[3]/ballradii[i]*3*np.pi)
	else:
		colorresult = 1.0

	if colorresult < 0.0:
		colorresult = 0.0

	return colorresult 

# Record the time before computation starts.

starttime = time.time()

# Iterate over two-dimensional grid of camera's vision.

for i in range(npoints):
	for j in range(npoints):
		# Start with negative angle. If it remains negative, then there was no intersect.
		minintersectangle = -1.0

		# A variable to determine which sphere intersects the light ray. Initialized to negative to indicate
		# that there is no intersect found yet.
		intersectsphere = -1

		# Find the current light direction.
		currentlight = mycam.lightdir(i,j)

		# Iterate over sphere k. Find if the light ray intersects sphere k.
		for k in range(nspheres):
			newangle = findintersectball( mycam.position, currentlight, listofballs[k])

			# If intersection angle is less than previously found or if no intersects were found yet,
			# then record the new intersect and set that sphere intersected is k.
			if newangle > 0 and (newangle < minintersectangle or minintersectangle < 0):
				minintersectangle = newangle
				intersectsphere = k

		# If an intersect was found, then find the intersect vector position. Then use this with ballcolormap
		# to find the color of the ball at this position.
		# If no intersect was found, then just use the default failcolor.

		if minintersectangle >= 0:
			intersect = np.cos(minintersectangle)*mycam.position + np.sin(minintersectangle)*currentlight
			visualpoints[i][j] = ballcolormap(intersectsphere, intersect)
		else:
			visualpoints[i][j] = failcolor

	# Print out when finished every 10th of job done. Let's the user know that the program is running correctly.

	if (i % (int(npoints/10)) == 0):
		print("Finished processing visualpoints["+str(i)+"][:]")

# Record the time when calculations finish. Find the total running time of the calculations.

endtime = time.time()
print ("Time to finish is %s seconds" % (endtime - starttime))

# Set up and print color grid.
		
xmesh, ymesh = np.meshgrid(np.array(range(npoints)),np.array(range(npoints))) 

plt.pcolor(xmesh, ymesh, visualpoints, cmap = 'CMRmap')# vmin = 0.0, vmaz = 1.0)
plt.axes().set_aspect('equal', 'datalim')
plt.axis('off')
plt.show()
