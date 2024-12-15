# Template
import argparse
from types import SimpleNamespace
from enum import Enum
from time import sleep


class Item(Enum):
	ROBOT = '@'
	SPACE = '.'
	BOX = 'O'
	WALL = '#'
	BIG_BOX = '[]'


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	mat = []
	movements = ''
	with open(f_name) as f:
		for line in f:
			line = line.strip()
			if line.startswith(Item.WALL.value):
				# mat.append(list(line))
				row = []
				for ch in line:
					if ch in [Item.WALL.value, Item.SPACE.value]:
						row.extend([ch] * 2)
					if ch == Item.BOX.value:
						row.extend(list(Item.BIG_BOX.value))
					if ch == Item.ROBOT.value:
						row.extend([ch, Item.SPACE.value])
				mat.append(row)
			elif line != '':
				movements += line
	return mat, movements


def pp(m):
	for line in m:
		print(''.join(line))
	print()


def solve(mat, movements):
	w, h = len(mat[0]), len(mat)
	robot = SimpleNamespace(x=0,y=0)
	for i, line in enumerate(mat):
		if (j := (line.index(Item.ROBOT.value) if Item.ROBOT.value in line else -1)) != -1:
			robot.x = i
			robot.y = j
			break
	print(mat, robot)


	moves = {
		'>': SimpleNamespace(y=1, x=0),
		'<': SimpleNamespace(y=-1, x=0),
		'^': SimpleNamespace(y=0, x=-1),
		'v': SimpleNamespace(y=0, x=1),
	}
	def _move(d):
		move = moves[d]
		curr = SimpleNamespace(**vars(robot))
		boxes = 0
		# Move until either find an empty space, or hit a wall
		while True:
			curr.x += move.x
			curr.y += move.y
			if mat[curr.x][curr.y] == Item.WALL.value:
				return
			if mat[curr.x][curr.y] == Item.SPACE.value:
				break
			if mat[curr.x][curr.y] == Item.BOX.value:
				boxes += 1

		mat[robot.x][robot.y] = Item.SPACE.value
		robot.x += move.x
		robot.y += move.y
		mat[robot.x][robot.y] = Item.ROBOT.value
		if boxes:
			mat[curr.x][curr.y] = Item.BOX.value


	def _move_big(d):
		move = moves[d]

		next_x = robot.x + move.x
		next_y = robot.y + move.y
		if mat[next_x][next_y] == Item.SPACE.value:
			# Swap robot and space
			mat[next_x][next_y], mat[robot.x][robot.y] = mat[robot.x][robot.y], mat[next_x][next_y]
			robot.x = next_x
			robot.y = next_y
			return

		if mat[next_x][next_y] == Item.WALL.value:
			# Wall, can not move
			return

		# Move until either find an empty space, or hit a wall
		if d in '<>':
			curr = SimpleNamespace(**vars(robot))
			boxes = 0
			# Easy case: left-right
			while True:
				curr.x += move.x
				curr.y += move.y
				if mat[curr.x][curr.y] == Item.WALL.value:
					return
				if mat[curr.x][curr.y] == Item.SPACE.value:
					break

				# Here, we know we have box
				boxes += 1
				curr.x += move.x
				curr.y += move.y

			if d == '<':
				mat[curr.x] = mat[curr.x][:curr.y] + mat[curr.x][curr.y + 1:robot.y + 1] + [Item.SPACE.value] + mat[curr.x][robot.y + 1:]
				robot.y += move.y
			if d == '>':
				mat[curr.x] = mat[curr.x][:robot.y] + [Item.SPACE.value] + mat[curr.x][robot.y:curr.y] + mat[curr.x][curr.y+1:]
				robot.y += move.y
		else:
			# Help...
			boxes_to_move = []
			if mat[next_x][robot.y] == '[':
				box = SimpleNamespace(x=next_x, y1=robot.y, y2=robot.y + 1)
			if mat[next_x][robot.y] == ']':
				box = SimpleNamespace(x=next_x, y1=robot.y - 1, y2=robot.y)
			boxes_to_move.append(box)

		

			idx = 0
			while True:
				btm = boxes_to_move[idx]
				next_x = btm.x + move.x
				# If can't move, return
				if mat[next_x][btm.y1] == Item.WALL.value or mat[next_x][btm.y2] == Item.WALL.value:
					return
				for y1, y2 in [(btm.y1 - 1, btm.y1), (btm.y1, btm.y2), (btm.y2, btm.y2 + 1)]:
					if mat[next_x][y1] == '[' and mat[next_x][y2] == ']':
						box = SimpleNamespace(x=next_x, y1=y1, y2=y2)
					if not box in boxes_to_move:
						boxes_to_move.append(box)
				idx += 1
				if idx >= len(boxes_to_move):
					break

			for btm in boxes_to_move[::-1]:
				mat[btm.x][btm.y1] = Item.SPACE.value
				mat[btm.x][btm.y2] = Item.SPACE.value
				mat[btm.x + move.x][btm.y1] = '['
				mat[btm.x + move.x][btm.y2] = ']'
			
			# Finally, move the robot
			first_btm = boxes_to_move[0]
			mat[first_btm.x][robot.y] = Item.ROBOT.value
			mat[robot.x][robot.y] = Item.SPACE.value
			robot.x = first_btm.x



	def _count_boxes(matrix):
		return sum([line.count('[') for line in matrix])
			
			


	print('Initial state:')
	pp(mat)
	boxes = _count_boxes(mat)
	for m in movements:
		_move_big(m)
		print(f'Move {m}:')
		pp(mat)
		
		if boxes != _count_boxes(mat):
			print('.' * 100)
			sleep(1)
			boxes = _count_boxes(mat)

	# coords_sum = 0
	# for x, line in enumerate(mat):
	# 	for y, ch in enumerate(line):
	# 		if ch == Item.BOX.value:
	# 			coords_sum += 100 * x + y
	# return coords_sum

	coords_sum = 0
	for x, line in enumerate(mat):
		for y, ch in enumerate(line):
			if ch == Item.BIG_BOX.value[0]:
				coords_sum += 100 * x + y
	return coords_sum



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve(*in_values)
	
	print(f'Result: {res}')