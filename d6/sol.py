from pprint import pprint
import copy


def read_in():
	obstacles = []
	guard_pos = (-1, -1)
	guard_dir = ''

	rows_cnt = 0
	with open('f.in') as f:
		for line in f:
			line_values = []
			for col, value in enumerate(line.strip()):
				if value == '.':
					line_values.append(False)
				elif value == '#':
					line_values.append(True)
				else:
					# Guard!!
					guard_dir = value
					guard_pos = (rows_cnt, col)
					line_values.append(False)
			obstacles.append(line_values)
			rows_cnt += 1
	return obstacles, guard_pos, guard_dir


def count_visits(obstacles, guard_pos, guard_dir):
	w, h = len(obstacles[0]), len(obstacles)
	directions_inc = {
		'^': [-1, 0],
		'>': [0, 1],
		'v': [1, 0],
		'<': [0, -1],
	}
	turns = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

	visited = []
	for i in range(h):
		line = []
		for j in range(w):
			vis = {'^': False, '>': False, 'v': False, '<': False, 'X': False}
			if (i, j) == guard_pos:
				vis[guard_dir] = True
				vis['X'] = True
			line.append(vis)
		visited.append(line)

	# pprint(visited)

	while True:
		# doamne-ajuta
		inc = directions_inc[guard_dir]
		next_pos = (guard_pos[0] + inc[0], guard_pos[1] + inc[1])
		# Boundaries check
		should_leave = next_pos[0] < 0 or next_pos[0] >= h or next_pos[1] < 0 or next_pos[1] >= w
		if should_leave:
			break
		# Obstacle check
		should_turn = obstacles[next_pos[0]][next_pos[1]]
		if should_turn:
			guard_dir = turns[guard_dir]
			continue

		# Tuuuurn
		if visited[next_pos[0]][next_pos[1]][guard_dir]:
			# If we've been here before in the same direction, we're done
			return -1

		visited[next_pos[0]][next_pos[1]][guard_dir] = True
		visited[next_pos[0]][next_pos[1]]['X'] = True
		guard_pos = next_pos

	total_vis = 0
	for line in visited:
		vis_count = sum([int(x['X']) for x in line])
		total_vis += vis_count
	return total_vis


def second_part():
	obstacles, guard_pos, guard_dir = read_in()
	w, h = len(obstacles[0]), len(obstacles)
	count = 0
	for i in range(w):
		for j in range(h):
			print(i, j)
			# Check what we have here:
			if guard_pos[0] == i and guard_pos[1] == j:
				continue
			if obstacles[i][j]:
				continue
			# Add obstacle and see if the guard gets stuck
			clone = copy.deepcopy(obstacles)
			clone[i][j] = True

			if count_visits(clone, guard_pos, guard_dir) == -1:
				count += 1
	return count




if __name__ == '__main__':
	res = second_part()
	
	print(f'Result: {res}')