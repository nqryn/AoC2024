# Template
import argparse
import re
from types import SimpleNamespace
from pprint import pprint
from time import sleep
from PIL import Image


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	pattern = r"p=(?P<x>\d+),(?P<y>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)"

	robots = []
	with open(f_name) as f:
		for line in f:
			# Remeber to line.strip() !!!!
			line = line.strip()
			match = re.search(pattern, line)
			if match:
				x, y, vx, vy = map(int, match.groups())
				robots.append(SimpleNamespace(x=x, y=y, vx=vx, vy=vy))

	return robots


def compute_location(w, h, robot, steps):
	cx, cy = robot.x, robot.y
	for _ in range(steps):
		cx = cx + robot.vx
		cy = cy + robot.vy
		if cx >= w:
			cx = cx % w
		if cx < 0:
			cx = w + cx
		if cy >= h:
			cy = cy % h
		if cy < 0:
			cy = h + cy
	return cx, cy


def nice_print(mat):
	for line in mat:
		for val in line:
			if not val:
				print(' ', end='')
			else:
				print('*', end='')
		print()





def img_gen(matrix, seconds):

	white = (255, 255, 255)
	green = (0, 255, 0) 

	height = len(matrix)
	width = len(matrix[0])

	# Create a new image
	image = Image.new('RGB', (width, height))

	# Set pixel values
	for y in range(height):
		for x in range(width):
			color = green if matrix[y][x] else white
			image.putpixel((x, y), color)

	# Save the image locally
	image.save(f"imgs/d14_{seconds}.png")



def solve2(robots):
	# w, h, steps = 11, 7, 100
	w, h, steps = 101, 103, 1
	seconds = 0
	while True:
		mat = []
		for _ in range(h):
			mat.append([0] * w)
		for r in robots:
			rx, ry = compute_location(w, h, r, steps)
			mat[ry][rx] += 1
			r.x, r.y = rx, ry


		img_gen(mat, seconds)
		# mid_w, mid_h = 50, 51
		# similar = True
		# for y in range(h):
		# 	for x in range(mid_w):
		# 		if mat[y][x] == 0 and mat[y][-x-1] > 0:
		# 			similar = False
		# 			break
		# 		if mat[y][x] > 0 and mat[y][-x-1] == 0:
		# 			similar = False
		# 			break
		# 	if not similar:
		# 		break
		# print(seconds)
		# if similar:
		# 	nice_print(mat)
		# 	print('_' * 103)
		# 	sleep(1)

		# qs = [0, 0, 0, 0]
		# mid_w, mid_h = 50, 51
		# for x in range(mid_w):
		# 	for y in range(mid_h):
		# 		qs[0] += mat[y][x]
		# 	for y in range(mid_h+1, h):
		# 		qs[1] += mat[y][x]
		# for x in range(mid_w+1,w):
		# 	for y in range(mid_h):
		# 		qs[2] += mat[y][x]
		# 	for y in range(mid_h+1, h):
		# 		qs[3] += mat[y][x]
		# if qs[0] == qs[1] and qs[2] == qs[3]:
		# 	nice_print(mat)
		# 	print('_' * 103)
		# 	print(seconds)
		# 	sleep(1)
		# sleep(1)
		
		seconds += 1



def solve(robots):
	# w, h, steps = 11, 7, 100
	w, h, steps = 101, 103, 100
	mat = []
	# mid_w, mid_h = 5, 3
	mid_w, mid_h = 50, 51
	for _ in range(h):
		mat.append([0] * w)
	for r in robots:
		rx, ry = compute_location(w, h, r, steps)
		mat[ry][rx] += 1

	qs = [0, 0, 0, 0]
	for x in range(mid_w):
		for y in range(mid_h):
			qs[0] += mat[y][x]
		for y in range(mid_h+1, h):
			qs[1] += mat[y][x]
	for x in range(mid_w+1,w):
		for y in range(mid_h):
			qs[2] += mat[y][x]
		for y in range(mid_h+1, h):
			qs[3] += mat[y][x]

	print(len(robots))
	print(sum(qs))
	return qs[0]*qs[1]*qs[2]*qs[3]



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	robots = read_in(args.test)
	res = solve2(robots)
	
	print(f'Result: {res}')