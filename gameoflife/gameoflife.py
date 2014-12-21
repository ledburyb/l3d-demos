from collections import defaultdict
from L3D import L3D

cube, dead_color = None, None

def setup():
  global cube, dead_color

  # size(displayWidth, displayHeight, P3D)
  size(800, 800, P3D)
  frameRate(10)

  dead_color = color(0, 0, 0)

  cube = L3D(this)
  cube.enableDrawing()
  cube.enableMulticastStreaming()
  cube.enablePoseCube()
  
  reset_cube()

def count_neighbors(x, y, z):
	neighbour_count = 0

	for i in range(x-1, x+2):
		for j in range(y-1, y+2):
			for k in range(z-1, z+2):
				if (i >= 0 and j >= 0 and k >= 0) and (i<=7 and j<=7 and k<=7) and ((i, j, k) != (x, y, z)) and not cube.getVoxel(i,j,k) == dead_color:
					neighbour_count += 1

	return neighbour_count

def reset_cube():
	cube.background(0);

	for i in range(8):
		for j in range(8):
			for k in range(8):
				voxel = PVector(i, j, k)
				if random(1) > 0.5:
					cube.setVoxel(voxel, (i+1)*255/8,(j+1)*255/8,(k+1)*255/8)
				else:
					cube.setVoxel(voxel, dead_color)

def tick():
	neighbour_count = 0;
	live_map = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))

	num_filled = 0

	# Don't make changes to the cube yet as updates must be simultaneous
	for i in range(8):
		for j in range(8):
			for k in range(8):
				neighbour_count = count_neighbors(i, j, k)
				voxel = PVector(i, j, k)
				if neighbour_count >= 5 and neighbour_count < 8:
					num_filled += 1
					live_map[i][j][k] = True
				else:
					cube.setVoxel(voxel, dead_color)

	cube.background(0)
	for i in range(8):
		for j in range(8):
			for k in range(8):
				voxel = PVector(i, j, k)
				if live_map[i][j][k]:
					cube.setVoxel(voxel, (i+1)*255/8,(j+1)*255/8,(k+1)*255/8)
				else:
					cube.setVoxel(voxel, dead_color)

	return bool(num_filled)

def draw():
  background(0)
  if not tick():
  	reset_cube()
