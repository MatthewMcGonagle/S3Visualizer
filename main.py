from S3Visualizer import *


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
	else:
		colorresult = 1.0

	if colorresult < 0.0:
		colorresult = 0.0

	return colorresult 

starttime = time.time()
for i in range(npoints):
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
