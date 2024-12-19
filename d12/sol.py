# Template
import argparse
import enum
from pprint import pprint


class Direction(enum.Enum):
	HORIZONTAL = 1
	VERTICAL = 2


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	mat = []
	with open(f_name) as f:
		for line in f:
			mat.append(line.strip())
	return mat




def compute_price(garden: list[str]) -> int:
	w, h = len(garden[0]), len(garden)
	visited = [[False] * w for _ in range(h)]

	def _is_in_bounds(x, y):
		return 0 <= x < h and 0 <= y < w

	def _get_perimeter_for_cell(curr_x, curr_y) -> int:
		per = 0
		for inc_x, inc_y in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
			new_x, new_y = curr_x + inc_x, curr_y + inc_y
			if not _is_in_bounds(new_x, new_y) or garden[new_x][new_y] != garden[curr_x][curr_y]:
				per += 1
		return per


	def _flood(curr_x: int, curr_y: int) -> (int, int):
		plant = garden[curr_x][curr_y]
		visited[curr_x][curr_y] = True
		next_vals = []
		area, perimeter = 1, _get_perimeter_for_cell(curr_x, curr_y)
		while True:
			for inc_x, inc_y in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
				new_x, new_y = curr_x + inc_x, curr_y + inc_y
				if _is_in_bounds(new_x, new_y) and not visited[new_x][new_y] and garden[new_x][new_y] == plant:
					next_vals.append((new_x, new_y))
					visited[new_x][new_y] = True
					area += 1
					perimeter += _get_perimeter_for_cell(new_x, new_y)
			if not next_vals:
				break
			curr_x, curr_y = next_vals.pop(0)
		return area, perimeter


	def _get_dir(p1: tuple[int], p2: tuple[int]) -> Direction:
		if p1[0] == p2[0]:
			return Direction.VERTICAL
		return Direction.HORIZONTAL


	def _get_sides_for_region(region: list[tuple[int]]) -> int:
		print(region)
		if len(region) <= 2:
			return 4
		p1, p2 = region[0], region[1]
		xs, ys = set([p1[0], p2[0]]), set([p1[1], p2[1]])
		direction = _get_dir(p1, p2)

		# lines = {x: [] for x in range(h)}
		# for x, y in region:
		# 	lines[x].append(y)

		# for x, line in lines.items():
		# 	if not line:
		# 		continue
		# 	sorted_line = sorted(line)
		# 	sub_region = [sorted_line[0]]
		# 	sub_regions = []
		# 	for y in sorted_line[1:]:
		# 		if y == sub_region[-1] + 1:
		# 			sub_region.append(y)
		# 		else:
		# 			sub_regions.append(sub_region)
		# 			sub_region = [y]
		# 	sub_regions.append(sub_region)
		# 	lines[x] = sub_regions

		# pprint(lines)

		# x = 0
		# while True:
		# 	if lines[x]:
		# 		break
		# 	x += 1

		# sides = 4

		# prev = x
		# for curr, line in lines.items()[x + 1:]:


		sides = 4
		for point in region[2:]:
			new_direction = _get_dir(p2, point)

			if direction == new_direction:
				continue

			if point[0] in xs and point[1] in ys:
				sides -= 2
			else:
				sides += 2

			xs.add(point[0])
			ys.add(point[1])

			p2 = point
			direction = new_direction


		return sides

	def _count_corners(p: tuple[int]) -> int:
		whatever = ''
		smth = ''
		plant = garden[p[0]][p[1]]
		directions = {
			'N': [-1, 0],
			'NE': [-1, 1],
			'E': [0, 1],
			'SE': [1, 1],
			'S': [1, 0],
			'SW': [1, -1],
			'W': [0, -1],
			'NW': [-1, -1]
		}

		for d, (i, j) in directions.items():
			x, y = p[0] + i, p[1] + j
			if len(d) == 1:
				whatever += 'X' if _is_in_bounds(x, y) and garden[x][y] == plant else 'O'
			smth += 'X' if _is_in_bounds(x, y) and garden[x][y] == plant else 'O'

		corners = 0
		if whatever in ['XXOO', 'XOOX', 'OOXX', 'OXXO']:
			corners += 1
		if whatever in ['XOOO', 'OXOO', 'OOXO', 'OOOX']:
			corners += 2

		smth += smth[0]
		for h in [0, 2, 4, 6]:
			if smth[h:h+3] == 'XOX':
				corners += 1

		return corners



	def _get_sides_for_region_final(region: list[tuple[int]]) -> int:
		if len(region) <= 2:
			return 4

		sides = 0
		for p in region:
			corners = _count_corners(p)
			# print(corners)
			sides += corners

		return sides


	def _get_sides_for_region_final_2(region, cm):
		if len(region) <= 2:
			return 4

		sides = 0
		for p in region:
			sides += cm[p[0]][p[1]]

		return sides


	def _flood_sides(curr_x: int, curr_y: int, cm) -> (int, int):
		plant = garden[curr_x][curr_y]
		visited[curr_x][curr_y] = True
		next_vals = []
		area = 0
		region = []
		while True:
			area += 1
			region.append((curr_x, curr_y))

			for inc_x, inc_y in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
				new_x, new_y = curr_x + inc_x, curr_y + inc_y
				if _is_in_bounds(new_x, new_y) and not visited[new_x][new_y] and garden[new_x][new_y] == plant:
					next_vals.append((new_x, new_y))
					visited[new_x][new_y] = True
			if not next_vals:
				break
			curr_x, curr_y = next_vals.pop()

		perimeter = _get_sides_for_region_final_2(region, cm)
		return area, perimeter

	def _compute_corners_map() -> list[list[int]]:
		mat = []
		for i in range(h):
			line = []
			for j in range(w):
				line.append(_count_corners((i, j)))
			mat.append(line)
		return mat

	cm = _compute_corners_map()
	pprint(cm)
	price = 0
	curr_x, curr_y = 0, 0
	while True:
		if not visited[curr_x][curr_y]:
			# area, perimeter = _flood(curr_x, curr_y)
			area, perimeter = _flood_sides(curr_x, curr_y, cm)
			print(f'{garden[curr_x][curr_y]} -> {area}, {perimeter}')
			price += area * perimeter
		curr_y += 1
		if curr_y >= w:
			curr_y = 0
			curr_x += 1
			if curr_x >= h:
				return price



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	mat = read_in(args.test)
	res = compute_price(mat)
	
	print(f'Result: {res}')