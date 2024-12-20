# Template
import argparse
from types import SimpleNamespace
from collections import defaultdict

from common.shortest_path import bfs_sp


def read_in(test_mode: bool):
	f_name = 'f_test.in' if test_mode else 'f.in'
	# Define vars here
	mat = []
	start, stop = -1, -1
	with open(f_name) as f:
		for i, line in enumerate(f):
			row = line.strip()
			if 'S' in row:
				start = SimpleNamespace(x=i, y=row.index('S'))
			if 'E' in row:
				stop = SimpleNamespace(x=i, y=row.index('E'))
			mat.append(row)
	return mat, start, stop


def _debug(mat, path):

	for i, line in enumerate(mat):
		for j, value in enumerate(line):
			if mat[i][j] == '.':
				node = SimpleNamespace(x=i, y=j)
				if node in path:
					print('O', end='')
				else:
					print('.', end='')
			else:
				print(mat[i][j], end='')
		print()


def solve(mat, start, stop):
	size = len(mat)
	print(start, stop)

	def _get_neighbours(curr_node):
		neighbours = []
		for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx = curr_node.x + i
			ny = curr_node.y + j
			if 0 <= nx < size and 0 <= ny < size and mat[nx][ny] != '#':
				neighbours.append(SimpleNamespace(x=nx, y=ny))
		return neighbours

	initial_sp = bfs_sp(start, stop, _get_neighbours)

	# print(initial_sp)
	threshold = 100
	# threshold = 50
	cheat_lens = defaultdict(int)
	sp_len = len(initial_sp)
	cheat_duration = 20
	print(f'Currently {sp_len} in path')

	# For each node starting from the beginning, we look to see what the best we can do which also respects min constraint
	for i, node1 in enumerate(initial_sp[:sp_len - threshold]):
		for j, node2 in enumerate(initial_sp[sp_len - 1:i + threshold:-1]):

			if (dur := (abs(node1.x - node2.x) + abs(node1.y - node2.y))) <= cheat_duration:
				picos_saved = sp_len - dur - 1 - j - i
				cheat_lens[sp_len - dur - 1 - j - i] += 1


	# for k, v in sorted(cheat_lens.items(), key=lambda x: x[0]):
	# 	print(f'There are {v} cheats that save {k} picoseconds.')
	
	total = 0
	for k, v in cheat_lens.items():
		if k >= threshold:
			total += v

	return total


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Process some flags.")
	parser.add_argument('--test', action='store_true', help="Run in test mode")
	args = parser.parse_args()

	in_values = read_in(args.test)
	res = solve(*in_values)
	
	print(f'Result: {res}')